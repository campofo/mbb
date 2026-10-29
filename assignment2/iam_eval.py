#!/usr/bin/env python3
"""iam_eval.py -- Part A1 of the Cloud IAM Audit assignment.

YOUR NAME:        Clement Ampofo
YOUR STUDENT ID:  <put your student id here>

A simplified-AWS IAM policy evaluator implementing the semantics described in
the assignment and primer. Python 3 standard library only.

Usage:
    python iam_eval.py <account.json> <requests.json> <out.json>

out.json is a JSON array, one object per request IN INPUT ORDER:
    {"id": ..., "decision": "ALLOW"|"DENY",
     "reason": "explicit_allow"|"explicit_deny"|"implicit_deny"}
"""
import ipaddress
import json
import re
import sys

ALLOW, DENY = "ALLOW", "DENY"
EXPLICIT_ALLOW, EXPLICIT_DENY, IMPLICIT_DENY = (
    "explicit_allow", "explicit_deny", "implicit_deny")


# --------------------------------------------------------------------------
# Wildcard matching ( '*' = any run of chars, '?' = exactly one char )
# --------------------------------------------------------------------------
def _wildcard_regex(pattern):
    """Translate a pattern using only '*' and '?' wildcards into a regex that
    matches the whole string. Every other character is matched literally."""
    out = ["^"]
    for ch in pattern:
        if ch == "*":
            out.append(".*")
        elif ch == "?":
            out.append(".")
        else:
            out.append(re.escape(ch))
    out.append("$")
    return "".join(out)


def action_matches(pattern, action):
    """Case-INSENSITIVE wildcard match. e.g. 's3:Get*' matches 's3:GetObject'."""
    return re.match(_wildcard_regex(pattern), action, re.IGNORECASE) is not None


def resource_matches(pattern, resource):
    """Case-SENSITIVE wildcard match."""
    return re.match(_wildcard_regex(pattern), resource) is not None


def _string_like(pattern, value):
    """StringLike: case-sensitive wildcard match."""
    return re.match(_wildcard_regex(pattern), value) is not None


# --------------------------------------------------------------------------
# Conditions
# --------------------------------------------------------------------------
_SUPPORTED_OPERATORS = {"Bool", "StringEquals", "StringLike", "IpAddress"}
_SUPPORTED_KEYS = {"aws:MultiFactorAuthPresent", "aws:SourceIp",
                   "aws:RequestedRegion"}


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _one_key_holds(operator, context_value, values):
    """True if the (operator, key) is satisfied by any of `values` (OR)."""
    for v in values:
        if operator == "Bool":
            if str(context_value).lower() == str(v).lower():
                return True
        elif operator == "StringEquals":
            if str(context_value) == str(v):
                return True
        elif operator == "StringLike":
            if _string_like(str(v), str(context_value)):
                return True
        elif operator == "IpAddress":
            try:
                if ipaddress.ip_address(str(context_value)) in \
                        ipaddress.ip_network(str(v), strict=False):
                    return True
            except ValueError:
                continue
    return False


def condition_holds(condition, context):
    """True if the optional Condition block is satisfied by `context`.

    Supports Bool, StringEquals, StringLike, IpAddress over keys
    aws:MultiFactorAuthPresent, aws:SourceIp, aws:RequestedRegion. A key named
    in the condition but absent from `context` makes the condition FALSE.
    Values for one key are OR-ed; keys/operators are AND-ed. No condition -> True.
    """
    if not condition:
        return True
    for operator, mapping in condition.items():
        if operator not in _SUPPORTED_OPERATORS:
            # Out-of-scope operators: no test depends on them. Treat a named
            # key as unsatisfiable to stay conservative.
            return False
        for key, value in mapping.items():
            if key not in context:          # absent key -> condition false
                return False
            if not _one_key_holds(operator, context[key], _as_list(value)):
                return False
    return True


# --------------------------------------------------------------------------
# Account helpers
# --------------------------------------------------------------------------
def _statements(doc):
    if not isinstance(doc, dict):
        return []
    s = doc.get("Statement", [])
    return [s] if isinstance(s, dict) else s


def _arn_tail(arn):
    """Return the 'user/name' | 'role/name' | 'group/name' tail of an IAM ARN."""
    parts = arn.split(":", 5)
    return parts[5] if len(parts) == 6 else ""


def _find_user(account, name):
    return next((u for u in account.get("users", []) if u["name"] == name), None)


def _find_role(account, name):
    return next((r for r in account.get("roles", []) if r["name"] == name), None)


def _find_group(account, name):
    return next((g for g in account.get("groups", []) if g["name"] == name), None)


def _managed(account, name):
    return account.get("managed_policies", {}).get(name)


def effective_policies(account, principal_arn):
    """Identity-based policy documents that apply to a user or role."""
    tail = _arn_tail(principal_arn)
    docs = []
    if tail.startswith("user/"):
        user = _find_user(account, tail[len("user/"):])
        if not user:
            return []
        for n in user.get("policies", []):
            doc = _managed(account, n)
            if doc:
                docs.append(doc)
        docs.extend(user.get("inline_policies", {}).values())
        for gname in user.get("groups", []):
            grp = _find_group(account, gname)
            if grp:
                for n in grp.get("policies", []):
                    doc = _managed(account, n)
                    if doc:
                        docs.append(doc)
                docs.extend(grp.get("inline_policies", {}).values())
    elif tail.startswith("role/"):
        role = _find_role(account, tail[len("role/"):])
        if not role:
            return []
        for n in role.get("policies", []):
            doc = _managed(account, n)
            if doc:
                docs.append(doc)
        docs.extend(role.get("inline_policies", {}).values())
    return docs


# --------------------------------------------------------------------------
# Core decision
# --------------------------------------------------------------------------
def _statement_matches(stmt, action, resource, context):
    if any(action_matches(p, action) for p in _as_list(stmt.get("Action"))):
        if any(resource_matches(p, resource)
               for p in _as_list(stmt.get("Resource"))):
            return condition_holds(stmt.get("Condition"), context)
    return False


def _decide(docs, action, resource, context):
    """Apply deny/allow/implicit over a set of policy documents (identity side)."""
    saw_allow = False
    for doc in docs:
        for stmt in _statements(doc):
            if _statement_matches(stmt, action, resource, context):
                if stmt.get("Effect") == "Deny":
                    return DENY, EXPLICIT_DENY
                if stmt.get("Effect") == "Allow":
                    saw_allow = True
    if saw_allow:
        return ALLOW, EXPLICIT_ALLOW
    return DENY, IMPLICIT_DENY


def evaluate_identity(account, principal_arn, action, resource, context):
    """Identity-policy-only decision (no trust policy)."""
    return _decide(effective_policies(account, principal_arn),
                   action, resource, context)


# ---- trust policy (sts:AssumeRole) ---------------------------------------
def _account_of(arn):
    parts = arn.split(":")
    return parts[4] if len(parts) > 4 else ""


def _principal_matches(principal, caller_arn):
    """Trust-policy Principal matching."""
    if principal == "*":
        return True
    if isinstance(principal, dict):
        if "AWS" in principal:
            for a in _as_list(principal["AWS"]):
                if a == "*" or a == caller_arn:
                    return True
                # arn:aws:iam::<acct>:root matches any principal of that account
                if a.endswith(":root"):
                    root_acct = _account_of(a)
                    if root_acct and root_acct == _account_of(caller_arn):
                        return True
        # {"Service": ...} never matches a user/role caller.
    return False


def evaluate_trust(account, caller_arn, role_arn, context):
    """Evaluate a role's trust policy for an sts:AssumeRole request."""
    tail = _arn_tail(role_arn)
    if not tail.startswith("role/"):
        return DENY, IMPLICIT_DENY
    role = _find_role(account, tail[len("role/"):])
    if not role:
        return DENY, IMPLICIT_DENY
    saw_allow = False
    for stmt in _statements(role.get("trust_policy")):
        if not any(action_matches(p, "sts:AssumeRole")
                   for p in _as_list(stmt.get("Action"))):
            continue
        if not _principal_matches(stmt.get("Principal"), caller_arn):
            continue
        if not condition_holds(stmt.get("Condition"), context):
            continue
        if stmt.get("Effect") == "Deny":
            return DENY, EXPLICIT_DENY
        if stmt.get("Effect") == "Allow":
            saw_allow = True
    if saw_allow:
        return ALLOW, EXPLICIT_ALLOW
    return DENY, IMPLICIT_DENY


def evaluate(account, request):
    """Evaluate ONE request. Return (decision, reason)."""
    principal = request["principal"]
    action = request["action"]
    resource = request.get("resource", "")
    context = request.get("context") or {}

    if action.lower() == "sts:assumerole":
        # Two-sided rule: caller identity AND the role's trust policy.
        decision, reason = evaluate_identity(
            account, principal, action, resource, context)
        if decision == DENY:
            return decision, reason
        return evaluate_trust(account, principal, resource, context)

    return evaluate_identity(account, principal, action, resource, context)


def main(argv):
    if len(argv) != 4:
        print("Usage: python iam_eval.py <account.json> <requests.json> <out.json>")
        return 1
    with open(argv[1], encoding="utf-8") as f:
        account = json.load(f)
    with open(argv[2], encoding="utf-8") as f:
        requests = json.load(f)

    results = []
    for request in requests:
        decision, reason = evaluate(account, request)
        results.append({"id": request.get("id"),
                        "decision": decision, "reason": reason})

    with open(argv[3], "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
