"""Stage 3a: deterministic flags over the tasks that report plain stderr. A flag is a CANDIDATE only."""
import json
R = [json.loads(l) for l in open("stage12.jsonl")]
plain = [r for r in R if "construct_error" not in r and r.get("stderr_plain")]
rows = []
for r in plain:
    n = r["n"]; s = r["signals"]; f = []
    if s.get("S2_images", {}).get("groups_ge2", 0) > 0: f.append(f"shared images ({s['S2_images']['distinct']} images for {n} samples, max {s['S2_images']['max_group']})")
    b = s.get("S3_longest_block", {})
    if b.get("groups_ge2", 0) > 0: f.append(f"shared text block ({b['groups_ge2']} blocks repeated, max {b['max_group']})")
    i = s["S5_identical_input"]
    if i["groups_ge2"] > 0: f.append(f"identical inputs ({i['groups_ge2']} repeated, max {i['max_group']})")
    for k, v in s.get("S1_metadata", {}).items():
        if v["distinct"] >= 10 and v["max_group"] <= 50 and v["groups_ge2"] >= 5:
            f.append(f"meta[{k}] ({v['distinct']} values, max {v['max_group']}, {v['groups_ge2']} repeated)")
    p = s["S4_id_prefix"]["minus_last_segment"]
    if 1 < p["distinct"] < n and p["groups_ge2"] >= 5 and p["max_group"] <= 50:
        f.append(f"id prefix ({p['distinct']} prefixes, max {p['max_group']})")
    rows.append({"task": r["task"], "n": n, "epochs": r["epochs"], "flags": f})
json.dump(rows, open("stage3a_flags.json", "w"), indent=1)
fl = [x for x in rows if x["flags"]]
print(f"{len(plain)} tasks with plain stderr; {len(fl)} flagged, {len(rows)-len(fl)} not flagged\n")
for x in fl:
    print(f"{x['task'].split('/')[1]:32} n={x['n']:<6} " + " | ".join(x["flags"]))
print("\nnot flagged:", ", ".join(x["task"].split("/")[1] for x in rows if not x["flags"]))
