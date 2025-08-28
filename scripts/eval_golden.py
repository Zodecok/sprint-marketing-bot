import json, sys, httpx

API = "http://127.0.0.1:8000/chat"

def run_case(case):
    q = case["q"]
    r = httpx.post(API, json={"query": q}, timeout=60)
    r.raise_for_status()
    data = r.json()
    answer = (data.get("answer") or "").lower()
    ok = True
    reasons = []
    for must in case.get("must_include", []):
        if must.lower() not in answer:
            ok = False
            reasons.append(f"missing: {must}")
    min_sources = int(case.get("min_sources", 0))
    if data.get("source_count", 0) < min_sources:
        ok = False
        reasons.append(f"source_count<{min_sources}")
    return ok, reasons, data.get("request_id")

def main(path):
    fails = 0
    for line in open(path, "r", encoding="utf-8"):
        if not line.strip():
            continue
        case = json.loads(line)
        ok, reasons, rid = run_case(case)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case['q']} (req={rid}) {'' if ok else ' | ' + '; '.join(reasons)}")
        if not ok:
            fails += 1
    print("\nSummary:", "OK" if fails == 0 else f"{fails} failing")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main("tests/golden.jsonl")
