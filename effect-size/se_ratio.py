"""Plain vs clustered SE on one eval log, using inspect_ai's own stderr() implementation.
usage: se_ratio.py LOG KEY   (KEY = a sample metadata field, or 'passage' = hash of longest >=200-char text block)"""
import hashlib, math, re, sys
from inspect_ai.log import read_eval_log
from inspect_ai.scorer import SampleScore, stderr
from inspect_ai.model import ContentText
log = read_eval_log(sys.argv[1]); key = sys.argv[2]
def text(s):
    if isinstance(s.input, str): return s.input
    return "\n".join(m.content if isinstance(m.content, str) else " ".join(c.text for c in m.content if isinstance(c, ContentText)) for m in s.input)
def cluster(s):
    if key == "passage":
        b = [x for x in re.split(r"\n\s*\n", text(s)) if len(x) >= 200]
        return hashlib.sha1(max(b, key=len).encode()).hexdigest() if b else f"solo-{s.id}"
    return str((s.metadata or {}).get(key))
scorer_name = next(iter(log.samples[0].scores))
scores = []
for s in log.samples:
    sc = s.scores[scorer_name]
    scores.append(SampleScore(score=sc, sample_id=s.id, sample_metadata={**(s.metadata or {}), "_cluster": cluster(s)}))
plain = stderr()(scores); clus = stderr(cluster="_cluster")(scores)
k = len({sc.sample_metadata["_cluster"] for sc in scores})
print(f"{log.eval.task}: n={len(scores)} clusters={k} scorer={scorer_name} headline={log.results.scores[0].metrics}")
print(f"  plain SE={plain:.4f}  clustered SE={clus:.4f}  ratio={clus/plain:.2f}  -> effective n ≈ {len(scores)/(clus/plain)**2:.0f}")
