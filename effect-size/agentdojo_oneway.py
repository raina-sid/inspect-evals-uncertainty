"""Plain vs clustered SE on AgentDojo's own released runs (no model calls).

Uses ethz-spylab/agentdojo @ 089ed46, runs/claude-3-7-sonnet-20250219/*/*/important_instructions/*.json.
One-way CR1 clustered SE by (suite, user task) and by (suite, injection task), plus the two-way
Cameron-Gelbach-Miller combination V_user + V_inj - V_cell.

    git clone https://github.com/ethz-spylab/agentdojo && cd agentdojo && git checkout 089ed46
    python agentdojo_oneway.py runs/claude-3-7-sonnet-20250219
"""
import collections, glob, json, math, sys

root = sys.argv[1] if len(sys.argv) > 1 else "runs/claude-3-7-sonnet-20250219"
rows = []
for p in glob.glob(f"{root}/*/*/important_instructions/*.json"):
    d = json.load(open(p))
    rows.append((d["suite_name"], d["user_task_id"], d["injection_task_id"], float(d["security"]), float(d["utility"])))

def meat(vals, keys):
    n = len(vals); m = sum(vals) / n; g = collections.defaultdict(float)
    for v, k in zip(vals, keys): g[k] += v - m
    G = len(g)
    return G / (G - 1) * sum(s * s for s in g.values()) / n ** 2

print(f"n={len(rows)}")
for name, idx in [("attack success (security)", 3), ("utility under attack", 4)]:
    x = [r[idx] for r in rows]; n = len(x); m = sum(x) / n
    plain = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1) / n)
    vu = meat(x, [(r[0], r[1]) for r in rows]); vi = meat(x, [(r[0], r[2]) for r in rows])
    vc = meat(x, [(r[0], r[1], r[2]) for r in rows]); two = math.sqrt(max(vu + vi - vc, 0))
    print(f"{name}: mean={m:.4f} plain={plain:.4f} | by user task {math.sqrt(vu):.4f} ({math.sqrt(vu)/plain:.2f}x)"
          f" | by injection task {math.sqrt(vi):.4f} ({math.sqrt(vi)/plain:.2f}x) | two-way {two:.4f} ({two/plain:.2f}x)")
