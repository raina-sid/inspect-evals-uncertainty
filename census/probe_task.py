"""Stages 1-2 for one registered task. Prints one JSON line. No model calls."""
import collections, hashlib, json, re, sys, warnings
warnings.filterwarnings("ignore")
import inspect_evals._registry  # noqa: F401
from inspect_ai._util.registry import registry_find, registry_info, registry_params
from inspect_ai.model import ContentImage, ContentText
name = sys.argv[1]
out = {"task": name}
def metric_list(m):
    if m is None: return []
    if isinstance(m, dict): return [x for v in m.values() for x in metric_list(v)]
    if isinstance(m, (list, tuple)): return [x for v in m for x in metric_list(v)]
    return [m]
def describe(m):
    try:
        info = registry_info(m); p = registry_params(m)
        return {"name": info.name, "params": {k: str(v)[:60] for k, v in (p or {}).items()}}
    except Exception:
        return {"name": getattr(m, "__name__", str(m))[:60], "params": {}}
try:
    fn = next(t for t in registry_find(lambda i: i.type == "task") if registry_info(t).name == name)
    task = fn()
except Exception as e:
    out["construct_error"] = f"{type(e).__name__}: {str(e)[:200]}"; print(json.dumps(out)); sys.exit()
mets = []
for sc in (task.scorer or []):
    try: mets += [describe(m) for m in metric_list(registry_info(sc).metadata.get("metrics"))]
    except Exception as e: mets.append({"name": f"<scorer metrics unreadable: {e}>"})
mets += [describe(m) for m in metric_list(task.metrics)]
out["metrics"] = mets
names = [m["name"] for m in mets]
def is_stderr(m): return m["name"].split("/")[-1] == "stderr"
def clus(m): return m["params"].get("cluster") not in (None, "None")
out["stderr_plain"] = any(is_stderr(m) and not clus(m) for m in mets)
out["stderr_cluster"] = [m["params"].get("cluster") for m in mets if is_stderr(m) and clus(m)]
out["stderr_wrapped"] = [m["name"] for m in mets if not is_stderr(m) and "stderr" in str(m["params"])]
ds = list(task.dataset); n = len(ds); out["n"] = n; out["epochs"] = str(task.epochs)
def texts(s):
    if isinstance(s.input, str): return [s.input]
    t = []
    for msg in s.input:
        c = msg.content
        if isinstance(c, str): t.append(c)
        else: t += [x.text for x in c if isinstance(x, ContentText)]
    return t
def images(s):
    if isinstance(s.input, str): return []
    return [hashlib.sha1(str(x.image).encode()).hexdigest() for msg in s.input if not isinstance(msg.content, str) for x in msg.content if isinstance(x, ContentImage)]
def summarize(counter):
    return {"distinct": len(counter), "max_group": max(counter.values()) if counter else 0,
            "groups_ge2": sum(1 for v in counter.values() if v >= 2)}
sig = {}
keys = collections.defaultdict(collections.Counter)
for s in ds:
    for k, v in (s.metadata or {}).items():
        if isinstance(v, (str, int, float, bool)) or v is None: keys[k][v] += 1
sig["S1_metadata"] = {k: summarize(c) for k, c in keys.items() if 1 < len(c) < n}
img = collections.Counter(h for s in ds for h in set(images(s)))
if img: sig["S2_images"] = summarize(img)
blk = collections.Counter()
for s in ds:
    blocks = [b for t in texts(s) for b in re.split(r"\n\s*\n", t) if len(b) >= 200]
    if blocks: blk[hashlib.sha1(max(blocks, key=len).encode()).hexdigest()] += 1
if blk: sig["S3_longest_block"] = summarize(blk)
pre = collections.Counter(re.split(r"[-_.:/]", str(s.id))[0] if re.search(r"[-_.:/]", str(s.id)) else "<none>" for s in ds)
pre2 = collections.Counter(re.sub(r"[-_.:/][^-_.:/]*$", "", str(s.id)) for s in ds)
sig["S4_id_prefix"] = {"first_segment": summarize(pre), "minus_last_segment": summarize(pre2)}
full = collections.Counter(hashlib.sha1("\n".join(texts(s)).encode()).hexdigest() for s in ds)
sig["S5_identical_input"] = summarize(full)
out["signals"] = sig
print(json.dumps(out, default=str))
