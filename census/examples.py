"""Stage 3b: for one flagged task, print example groups behind each structural signal (2 groups x 2
samples), so a person can tell a cluster (shared item/context) from a template or a stratum."""
import collections, hashlib, json, re, sys, warnings
warnings.filterwarnings("ignore")
import inspect_evals._registry  # noqa
from inspect_ai._util.registry import registry_find, registry_info
from inspect_ai.model import ContentImage, ContentText
name, flagkeys = sys.argv[1], json.loads(sys.argv[2])
fn = next(t for t in registry_find(lambda i: i.type == "task") if registry_info(t).name == name)
ds = list(fn().dataset)
def texts(s):
    if isinstance(s.input, str): return [s.input]
    t = []
    for m in s.input:
        t += [m.content] if isinstance(m.content, str) else [x.text for x in m.content if isinstance(x, ContentText)]
    return t
def imgs(s):
    if isinstance(s.input, str): return []
    return [hashlib.sha1(str(x.image).encode()).hexdigest() for m in s.input if not isinstance(m.content, str) for x in m.content if isinstance(x, ContentImage)]
def block(s):
    b = [x for t in texts(s) for x in re.split(r"\n\s*\n", t) if len(x) >= 200]
    return max(b, key=len) if b else None
def show(s):
    t = " ".join(texts(s)).replace("\n", " ")
    return f"    id={s.id} target={str(s.target)[:40]!r} meta={ {k: str(v)[:30] for k, v in list((s.metadata or {}).items())[:4]} }\n      input[-220:]={t[-220:]!r}"
groupers = {"block": block, "identical": lambda s: hashlib.sha1("\n".join(texts(s)).encode()).hexdigest(),
            "image": lambda s: (imgs(s) or [None])[0]}
for fk in flagkeys:
    g = groupers[fk] if fk in groupers else (lambda s, k=fk: (s.metadata or {}).get(k))
    groups = collections.defaultdict(list)
    for s in ds:
        k = g(s)
        if k is not None: groups[k].append(s)
    rep = [v for v in groups.values() if len(v) >= 2]
    sizes = sorted((len(v) for v in rep), reverse=True)
    print(f"  [{fk}] {len(rep)} repeated groups; sizes top {sizes[:6]}; samples in repeated groups {sum(sizes)}/{len(ds)}")
    if fk == "block" and rep:
        big = max(rep, key=len); print(f"    largest shared block starts: {block(big[0])[:160]!r}")
    for grp in (rep[:1] + rep[len(rep)//2:len(rep)//2+1]):
        for s in grp[:2]: print(show(s))
