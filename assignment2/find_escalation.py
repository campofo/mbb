#!/usr/bin/env python3
"""find_escalation.py -- Part A2 of the Cloud IAM Audit assignment.

YOUR NAME:        Clement Ampofo
YOUR STUDENT ID:  <put your student id here>

Find every non-admin user or role that can reach an admin-equivalent identity,
and report a SHORTEST attack path for each. Python 3 standard library only.

Usage:
    python find_escalation.py <account.json> <out.json>
"""
import json
import sys
from collections import deque

import iam_eval
from iam_eval import (ALLOW, _as_list, _find_group, _find_role, _find_user,
                      _managed, _statements, evaluate, evaluate_identity)

ADMIN = "ADMIN"


# --------------------------------------------------------------------------
# ARN helpers
# --------------------------------------------------------------------------
def _acct(account):
    return account.get("account_id", "")


def user_arn(account, name):
    return f"arn:aws:iam::{_acct(account)}:user/{name}"


def role_arn(account, name):
    return f"arn:aws:iam::{_acct(account)}:role/{name}"


def group_arn(account, name):
    return f"arn:aws:iam::{_acct(account)}:group/{name}"


def policy_arn(account, name):
    return f"arn:aws:iam::{_acct(account)}:policy/{name}"


# --------------------------------------------------------------------------
# Admin-equivalence (fixed admin-probe set, empty context)
# --------------------------------------------------------------------------
def _probes(account):
    a = _acct(account)
    return [
        ("iam:CreateUser", f"arn:aws:iam::{a}:user/*"),
        ("s3:DeleteBucket", "arn:aws:s3:::*"),
        ("ec2:TerminateInstances",
         f"arn:aws:ec2:us-east-1:{a}:instance/*"),
        ("kms:ScheduleKeyDeletion",
         f"arn:aws:kms:us-east-1:{a}:key/*"),
    ]


def _allows(account, principal_arn, action, resource):
    """Full evaluation (two-sided for sts:AssumeRole) under an empty context."""
    decision, _ = evaluate(account, {"principal": principal_arn,
                                     "action": action, "resource": resource,
                                     "context": {}})
    return decision == ALLOW


def _identity_allows(account, principal_arn, action, resource):
    """Identity-policy-only allow under an empty context."""
    decision, _ = evaluate_identity(account, principal_arn, action, resource, {})
    return decision == ALLOW


def is_admin_equivalent(account, principal_arn):
    """True iff ALLOWED every probe under an empty context."""
    return all(_allows(account, principal_arn, act, res)
               for act, res in _probes(account))


def _group_docs(account, group):
    docs = [_managed(account, n) for n in group.get("policies", [])]
    docs = [d for d in docs if d]
    docs.extend(group.get("inline_policies", {}).values())
    return docs


def group_is_admin_equivalent(account, group):
    """A group is admin-equivalent iff its OWN policies allow all four probes."""
    from iam_eval import _decide
    for act, res in _probes(account):
        decision, _ = _decide(_group_docs(account, group), act, res, {})
        if decision != ALLOW:
            return False
    return True


# --------------------------------------------------------------------------
# Effective managed-policy names for a principal (for CreatePolicyVersion)
# --------------------------------------------------------------------------
def _effective_managed_names(account, principal_arn):
    tail = iam_eval._arn_tail(principal_arn)
    names = []
    if tail.startswith("user/"):
        user = _find_user(account, tail[len("user/"):])
        if user:
            names.extend(user.get("policies", []))
            for gname in user.get("groups", []):
                grp = _find_group(account, gname)
                if grp:
                    names.extend(grp.get("policies", []))
    elif tail.startswith("role/"):
        role = _find_role(account, tail[len("role/"):])
        if role:
            names.extend(role.get("policies", []))
    # keep only names that resolve to a real managed policy
    return [n for n in names if _managed(account, n)]


# --------------------------------------------------------------------------
# Trust-policy service check (for PassRole techniques)
# --------------------------------------------------------------------------
def _trust_allows_service(role, service):
    for stmt in _statements(role.get("trust_policy")):
        if stmt.get("Effect") != "Allow":
            continue
        if not any(iam_eval.action_matches(p, "sts:AssumeRole")
                   for p in _as_list(stmt.get("Action"))):
            continue
        principal = stmt.get("Principal")
        if isinstance(principal, dict) and service in _as_list(
                principal.get("Service")):
            return True
    return False


# --------------------------------------------------------------------------
# Edge generation (one check per catalogue technique, empty context)
# --------------------------------------------------------------------------
def generate_edges(account):
    """Return a list of (from_arn, technique, to_arn_or_ADMIN) edges."""
    acct = _acct(account)
    users = account.get("users", [])
    roles = account.get("roles", [])
    admin_groups = [g for g in account.get("groups", [])
                    if group_is_admin_equivalent(account, g)]

    # every principal that can be a source (users and roles)
    sources = [("user", u["name"], user_arn(account, u["name"])) for u in users]
    sources += [("role", r["name"], role_arn(account, r["name"])) for r in roles]

    edges = []
    for kind, name, p_arn in sources:
        # 1. CreateAccessKey  (another user)
        for u in users:
            if u["name"] == name and kind == "user":
                continue
            target = user_arn(account, u["name"])
            if _allows(account, p_arn, "iam:CreateAccessKey", target):
                edges.append((p_arn, "CreateAccessKey", target))

        # 2. CreateLoginProfile / UpdateLoginProfile  (another user)
        for u in users:
            if u["name"] == name and kind == "user":
                continue
            target = user_arn(account, u["name"])
            if _allows(account, p_arn, "iam:CreateLoginProfile", target):
                edges.append((p_arn, "CreateLoginProfile", target))
            elif _allows(account, p_arn, "iam:UpdateLoginProfile", target):
                edges.append((p_arn, "UpdateLoginProfile", target))

        # 3. AssumeRole  (two-sided)
        for r in roles:
            if r["name"] == name and kind == "role":
                continue
            target = role_arn(account, r["name"])
            if _allows(account, p_arn, "sts:AssumeRole", target):
                edges.append((p_arn, "AssumeRole", target))

        # 4. PassRole+RunInstances(EC2)
        ec2_res = f"arn:aws:ec2:us-east-1:{acct}:instance/*"
        for r in roles:
            if not _trust_allows_service(r, "ec2.amazonaws.com"):
                continue
            target = role_arn(account, r["name"])
            if _allows(account, p_arn, "iam:PassRole", target) and \
                    _allows(account, p_arn, "ec2:RunInstances", ec2_res):
                edges.append((p_arn, "PassRole+RunInstances(EC2)", target))

        # 5. PassRole+CreateFunction(Lambda)
        fn_res = f"arn:aws:lambda:us-east-1:{acct}:function:*"
        for r in roles:
            if not _trust_allows_service(r, "lambda.amazonaws.com"):
                continue
            target = role_arn(account, r["name"])
            if _allows(account, p_arn, "iam:PassRole", target) and \
                    _allows(account, p_arn, "lambda:CreateFunction", fn_res) and \
                    _allows(account, p_arn, "lambda:InvokeFunction", fn_res):
                edges.append((p_arn, "PassRole+CreateFunction(Lambda)", target))

        # 6. UpdateAssumeRolePolicy+AssumeRole  (identity-only AssumeRole)
        for r in roles:
            if r["name"] == name and kind == "role":
                continue
            target = role_arn(account, r["name"])
            if _allows(account, p_arn, "iam:UpdateAssumeRolePolicy", target) and \
                    _identity_allows(account, p_arn, "sts:AssumeRole", target):
                edges.append(
                    (p_arn, "UpdateAssumeRolePolicy+AssumeRole", target))

        # 7/8. AttachUserPolicy/PutUserPolicy (self) -> ADMIN  (users only)
        if kind == "user":
            if _allows(account, p_arn, "iam:AttachUserPolicy", p_arn):
                edges.append((p_arn, "AttachUserPolicy(self)", ADMIN))
            if _allows(account, p_arn, "iam:PutUserPolicy", p_arn):
                edges.append((p_arn, "PutUserPolicy(self)", ADMIN))

        # 9. AddUserToGroup(admin) -> ADMIN
        for g in admin_groups:
            if _allows(account, p_arn, "iam:AddUserToGroup",
                       group_arn(account, g["name"])):
                edges.append((p_arn, "AddUserToGroup(admin)", ADMIN))

        # 10. CreatePolicyVersion(self-policy) -> ADMIN
        for pname in _effective_managed_names(account, p_arn):
            if _allows(account, p_arn, "iam:CreatePolicyVersion",
                       policy_arn(account, pname)):
                edges.append((p_arn, "CreatePolicyVersion(self-policy)", ADMIN))
                break

        # 11/12. AttachRolePolicy/PutRolePolicy (self) -> ADMIN  (roles only)
        if kind == "role":
            if _allows(account, p_arn, "iam:AttachRolePolicy", p_arn):
                edges.append((p_arn, "AttachRolePolicy(self)", ADMIN))
            if _allows(account, p_arn, "iam:PutRolePolicy", p_arn):
                edges.append((p_arn, "PutRolePolicy(self)", ADMIN))

    return edges


# --------------------------------------------------------------------------
# Graph search
# --------------------------------------------------------------------------
def find_escalations(account):
    users = account.get("users", [])
    roles = account.get("roles", [])

    all_principals = [user_arn(account, u["name"]) for u in users] + \
                     [role_arn(account, r["name"]) for r in roles]
    admin_set = {p for p in all_principals
                 if is_admin_equivalent(account, p)}

    # adjacency: source -> sorted list of (technique, to)
    adj = {p: [] for p in all_principals}
    for frm, tech, to in generate_edges(account):
        adj.setdefault(frm, []).append((tech, to))
    for p in adj:
        adj[p] = sorted(adj[p], key=lambda e: (e[0], e[1]))

    def is_goal(node):
        return node == ADMIN or node in admin_set

    escalations = []
    for start in sorted(p for p in all_principals if p not in admin_set):
        path = _bfs(start, adj, is_goal)
        if path is not None:
            escalations.append({"principal": start, "path": path})

    escalations.sort(key=lambda e: e["principal"])
    return {"admin_equivalent": sorted(admin_set),
            "escalations": escalations}


def _bfs(start, adj, is_goal):
    """Shortest path from `start` to a goal node. Neighbours are expanded in the
    pre-sorted (technique, to) order; the first shortest path found is kept."""
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        for tech, to in adj.get(node, []):
            step = {"from": node, "technique": tech, "to": to}
            if is_goal(to):
                return path + [step]
            if to not in visited:
                visited.add(to)
                queue.append((to, path + [step]))
    return None


def main(argv):
    if len(argv) != 3:
        print("Usage: python find_escalation.py <account.json> <out.json>")
        return 1
    with open(argv[1], encoding="utf-8") as f:
        account = json.load(f)
    result = find_escalations(account)
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
