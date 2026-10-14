import json, os, shutil, subprocess, sys, warnings
warnings.filterwarnings("ignore")
import inspect_evals._registry  # noqa
from inspect_ai._util.registry import registry_find, registry_info
OUT = sys.argv[1]; PROBE = os.path.join(os.path.dirname(__file__), "probe_task.py")
names = sorted(registry_info(t).name for t in registry_find(lambda i: i.type == "task"))
done = {json.loads(l)["task"] for l in open(OUT)} if os.path.exists(OUT) else set()
for i, n in enumerate(names):
    if n in done: continue
    if shutil.disk_usage("/System/Volumes/Data").free < 20e9: print("disk guard", flush=True); break
    try:
        r = subprocess.run([sys.executable, PROBE, n], capture_output=True, text=True, timeout=600)
        line = next((l for l in reversed(r.stdout.strip().splitlines()) if l.startswith("{")), None)
        rec = json.loads(line) if line else {"task": n, "construct_error": "no output: " + r.stderr.strip()[-200:]}
    except subprocess.TimeoutExpired:
        rec = {"task": n, "construct_error": "timeout 600s"}
    with open(OUT, "a") as f: f.write(json.dumps(rec, default=str) + "\n")
    print(i, n, "ERR" if "construct_error" in rec else f"n={rec.get('n')} plain={rec.get('stderr_plain')}", flush=True)
