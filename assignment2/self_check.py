#!/usr/bin/env python3
"""Self-check for the Cloud IAM Audit assignment.

Run this from the folder that holds your submission files, with the provided
account.json, requirements.json, requests_public.json and expected_public.json
alongside them (all provided to you):

    python self_check.py

This is NOT the marking script and does not compute a grade. It checks the
things most submissions get wrong before you hand in:

  A1  runs your iam_eval.py on the PUBLIC requests and compares your decisions
      and reasons to the provided expected answers, and independently validates
      your output schema.
  A2  runs your find_escalation.py and independently validates the output
      schema, sorting, technique names (must be exactly the catalogue's names)
      and that every path chains from the principal to ADMIN or an
      admin-equivalent identity. It does not tell you the right escalations.
  A3  independently checks account_fixed.json: valid JSON, same principal
      inventory as account.json, and no non-admin identity keeps Action "*" or
      "<svc>:*" on Resource "*". It also runs YOUR evaluator on the
      requirements.json must_allow/must_deny requests (only as reliable as your
      evaluator -- the marker uses the reference one).

Passing every check is necessary, not sufficient, for full marks: the real
marking also re-runs your code on a larger hidden request set and on a second
account, verifies every escalation path, and reads your writeup.pdf.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECISIONS = {"ALLOW", "DENY"}
# The exact technique names from the assignment's escalation catalogue.
TECHNIQUES = {
    "CreateAccessKey", "CreateLoginProfile", "UpdateLoginProfile", "AssumeRole",
    "PassRole+RunInstances(EC2)", "PassRole+CreateFunction(Lambda)",
    "UpdateAssumeRolePolicy+AssumeRole", "AttachUserPolicy(self)",
    "PutUserPolicy(self)", "AddUserToGroup(admin)",
    "CreatePolicyVersion(self-policy)", "AttachRolePolicy(self)",
    "PutRolePolicy(self)",
}
REASONS = {"explicit_allow", "explicit_deny", "implicit_deny"}


def run(cmd):
    try:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return None, "", "TIMEOUT after 60s -- check for an infinite loop"


def need(filename):
    if not os.path.isfile(os.path.join(HERE, filename)):
        print(f"[FAIL] {filename} not found in {HERE}")
        return False
    return True


def load(filename):
    with open(os.path.join(HERE, filename), encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
def check_a1():
    print("A1. Running your iam_eval.py on the public requests...")
    out_path = os.path.join(HERE, "_selfcheck_a1_out.json")
    rc, _, err = run([sys.executable, "iam_eval.py", "account.json",
                      "requests_public.json", out_path])
    if rc != 0 or not os.path.isfile(out_path):
        print(f"   [FAIL] iam_eval.py did not run cleanly (exit {rc}).")
        print(f"          stderr: {err or '(none)'}")
        return
    try:
        got = json.load(open(out_path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"   [FAIL] your out.json is not valid JSON: {e}")
        os.remove(out_path)
        return
    expected = load("expected_public.json")

    # Independent schema validation.
    schema_ok = True
    if not isinstance(got, list) or len(got) != len(expected):
        print(f"   [FAIL] expected a JSON array of {len(expected)} results, "
              f"got {type(got).__name__} of length "
              f"{len(got) if isinstance(got, list) else 'n/a'}.")
        schema_ok = False
    else:
        for i, item in enumerate(got):
            if (not isinstance(item, dict) or "id" not in item
                    or item.get("decision") not in DECISIONS
                    or item.get("reason") not in REASONS):
                print(f"   [FAIL] result #{i} has a bad schema: {item!r}")
                schema_ok = False
                break
    if schema_ok:
        print("   [PASS] output schema looks right (id/decision/reason, valid values).")

    by_id = {r["id"]: r for r in got if isinstance(r, dict)}
    dec_ok = sum(1 for e in expected
                 if by_id.get(e["id"], {}).get("decision") == e["decision"])
    rea_ok = sum(1 for e in expected
                 if by_id.get(e["id"], {}).get("decision") == e["decision"]
                 and by_id.get(e["id"], {}).get("reason") == e["reason"])
    n = len(expected)
    print(f"   decisions correct: {dec_ok}/{n}; decision+reason correct: {rea_ok}/{n}")
    if dec_ok < n:
        wrong = [e["id"] for e in expected
                 if by_id.get(e["id"], {}).get("decision") != e["decision"]]
        print(f"   [note] wrong decisions on: {', '.join(wrong)}")
    os.remove(out_path)


def check_a2():
    print("A2. Running your find_escalation.py and checking the output schema...")
    out_path = os.path.join(HERE, "_selfcheck_a2_out.json")
    rc, _, err = run([sys.executable, "find_escalation.py", "account.json", out_path])
    if rc != 0 or not os.path.isfile(out_path):
        print(f"   [FAIL] find_escalation.py did not run cleanly (exit {rc}).")
        print(f"          stderr: {err or '(none)'}")
        return
    try:
        result = json.load(open(out_path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"   [FAIL] your out.json is not valid JSON: {e}")
        os.remove(out_path)
        return

    ok = True
    if not isinstance(result, dict) or "admin_equivalent" not in result \
            or "escalations" not in result:
        print("   [FAIL] top level must be an object with 'admin_equivalent' "
              "and 'escalations'.")
        ok = False
    else:
        if not isinstance(result["admin_equivalent"], list) \
                or not all(isinstance(x, str) for x in result["admin_equivalent"]):
            print("   [FAIL] 'admin_equivalent' must be a list of ARN strings.")
            ok = False
        for e in (result["escalations"] if isinstance(result["escalations"], list) else []):
            if not isinstance(e, dict) or "principal" not in e or "path" not in e \
                    or not isinstance(e["path"], list):
                print(f"   [FAIL] bad escalation entry: {e!r}")
                ok = False
                break
            for step in e["path"]:
                if not isinstance(step, dict) or set(step) < {"from", "technique", "to"}:
                    print(f"   [FAIL] a path step is missing from/technique/to: {step!r}")
                    ok = False
                    break
    if ok:
        # Independent consistency checks on every reported path.
        admins = set(result["admin_equivalent"])
        for e in result["escalations"]:
            path, who = e["path"], e["principal"]
            problems = []
            if not path:
                problems.append("empty path")
            else:
                if path[0]["from"] != who:
                    problems.append("first step does not start at the principal")
                for a, b in zip(path, path[1:]):
                    if a["to"] != b["from"]:
                        problems.append("steps do not chain (to != next from)")
                        break
                if path[-1]["to"] != "ADMIN" and path[-1]["to"] not in admins:
                    problems.append("last step ends neither at ADMIN nor at an "
                                    "admin_equivalent identity")
                bad = sorted({st["technique"] for st in path} - TECHNIQUES)
                if bad:
                    problems.append(f"unknown technique name(s) {bad} -- use the exact "
                                    "names from the catalogue")
                if who in admins:
                    problems.append("principal is itself admin_equivalent (report "
                                    "non-admins only)")
            if problems:
                ok = False
                print(f"   [FAIL] {who}: " + "; ".join(problems))
        if result["admin_equivalent"] != sorted(result["admin_equivalent"]):
            print("   [FAIL] 'admin_equivalent' must be sorted.")
            ok = False
        prins = [e["principal"] for e in result["escalations"]]
        if prins != sorted(prins):
            print("   [FAIL] 'escalations' must be sorted by principal ARN.")
            ok = False
    if ok:
        n = len(result["escalations"]) if isinstance(result.get("escalations"), list) else 0
        print(f"   [PASS] schema and path consistency look right. You reported "
              f"{len(result.get('admin_equivalent', []))} admin-equivalent identities "
              f"and {n} escalations (correctness is checked by the marker).")
    os.remove(out_path)


def check_a3():
    print("A3. Independently checking account_fixed.json...")
    if not need("account_fixed.json"):
        return
    try:
        fixed = load("account_fixed.json")
    except Exception as e:  # noqa: BLE001
        print(f"   [FAIL] account_fixed.json is not valid JSON: {e}")
        return
    base = load("account.json")

    def inventory(acct):
        return (
            sorted(x["name"] for x in acct.get("users", [])),
            sorted(x["name"] for x in acct.get("roles", [])),
            sorted(x["name"] for x in acct.get("groups", [])),
        )

    if inventory(fixed) != inventory(base):
        print("   [FAIL] the set of user/role/group NAMES changed. You may edit "
              "policies, attachments and trust policies, but not add or remove "
              "principals.")
    else:
        print("   [PASS] principal inventory (users/roles/groups) unchanged.")

    # Wildcard-budget: no non-admin identity may keep "*" or "svc:*" on "*".
    designated = set()
    try:
        designated = set(load("requirements.json").get("designated_admins", []))
    except Exception:  # noqa: BLE001
        print("   [note] could not read requirements.json; skipping admin exemptions.")

    acct_id = fixed.get("account_id", "")
    mp = fixed.get("managed_policies", {})

    def statements(doc):
        s = doc.get("Statement", []) if isinstance(doc, dict) else []
        return [s] if isinstance(s, dict) else s

    def as_list(v):
        return [v] if isinstance(v, str) else (v or [])

    def is_blanket(stmt):
        if stmt.get("Effect") != "Allow":
            return False
        if "*" not in as_list(stmt.get("Resource")):
            return False
        for a in as_list(stmt.get("Action")):
            if a == "*" or (a.endswith(":*") and a.count("*") == 1):
                return True
        return False

    def arn_of(kind, name):
        return f"arn:aws:iam::{acct_id}:{kind}/{name}"

    def docs_for_user(user):
        docs = []
        for n in user.get("policies", []):
            if n in mp:
                docs.append(mp[n])
        docs += list(user.get("inline_policies", {}).values())
        for gname in user.get("groups", []):
            grp = next((g for g in fixed.get("groups", []) if g["name"] == gname), None)
            if grp:
                docs += [mp[n] for n in grp.get("policies", []) if n in mp]
                docs += list(grp.get("inline_policies", {}).values())
        return docs

    violations = []
    for user in fixed.get("users", []):
        arn = arn_of("user", user["name"])
        if arn in designated:
            continue
        if any(is_blanket(s) for d in docs_for_user(user) for s in statements(d)):
            violations.append(arn)
    for role in fixed.get("roles", []):
        arn = arn_of("role", role["name"])
        if arn in designated:
            continue
        docs = [mp[n] for n in role.get("policies", []) if n in mp]
        docs += list(role.get("inline_policies", {}).values())
        if any(is_blanket(s) for d in docs for s in statements(d)):
            violations.append(arn)

    check_requirements_with_own_evaluator()

    if violations:
        print("   [FAIL] these non-admin identities still have a blanket "
              "Action '*'/'<svc>:*' on Resource '*':")
        for v in violations:
            print(f"            {v}")
    else:
        print("   [PASS] no non-admin identity has a blanket wildcard on Resource '*'.")


def check_requirements_with_own_evaluator():
    """Run YOUR iam_eval.py on requirements.json's must_allow / must_deny
    requests against account_fixed.json. Only as trustworthy as your evaluator:
    the marker uses the reference evaluator instead."""
    try:
        req = load("requirements.json")
    except Exception:  # noqa: BLE001
        return
    reqs = [dict(r, id="allow:" + r["id"]) for r in req.get("must_allow", [])]
    reqs += [dict(r, id="deny:" + r["id"]) for r in req.get("must_deny", [])]
    in_path = os.path.join(HERE, "_selfcheck_a3_req.json")
    out_path = os.path.join(HERE, "_selfcheck_a3_out.json")
    with open(in_path, "w", encoding="utf-8") as f:
        json.dump(reqs, f)
    try:
        rc, _, err = run([sys.executable, "iam_eval.py", "account_fixed.json",
                          in_path, out_path])
        if rc != 0 or not os.path.isfile(out_path):
            print("   [note] could not check requirements.json with your iam_eval.py "
                  f"(exit {rc}); fix Part A1 first.")
            return
        got = {r.get("id"): r.get("decision") for r in json.load(open(out_path, encoding="utf-8"))
               if isinstance(r, dict)}
        bad_allow = [r["id"][6:] for r in reqs if r["id"].startswith("allow:") and got.get(r["id"]) != "ALLOW"]
        bad_deny = [r["id"][5:] for r in reqs if r["id"].startswith("deny:") and got.get(r["id"]) != "DENY"]
        tag = "PASS" if not (bad_allow or bad_deny) else "FAIL"
        print(f"   [{tag}] (using YOUR evaluator) must_allow still ALLOW: "
              f"{len(req.get('must_allow', [])) - len(bad_allow)}/{len(req.get('must_allow', []))}"
              f"{' -- failing ' + ', '.join(bad_allow) if bad_allow else ''}; "
              f"must_deny now DENY: {len(req.get('must_deny', [])) - len(bad_deny)}/{len(req.get('must_deny', []))}"
              f"{' -- failing ' + ', '.join(bad_deny) if bad_deny else ''}")
    except Exception as e:  # noqa: BLE001
        print(f"   [note] requirements check failed: {e}")
    finally:
        for p in (in_path, out_path):
            if os.path.exists(p):
                os.remove(p)


def main():
    required = ["iam_eval.py", "find_escalation.py", "account_fixed.json",
                "account.json", "requirements.json",
                "requests_public.json", "expected_public.json"]
    missing = [f for f in required if not os.path.isfile(os.path.join(HERE, f))]
    if missing:
        print(f"[FAIL] missing files in {HERE}: {missing}")
        print("Put self_check.py next to your submission and the provided files.")
        sys.exit(1)

    check_a1()
    print()
    check_a2()
    print()
    check_a3()
    print("\nDone. This does not check your writeup.pdf (Part A4) -- that is "
          "marked by a human.")


if __name__ == "__main__":
    main()
