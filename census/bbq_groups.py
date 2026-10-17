"""BBQ cluster key used by the census: the AMBIGUOUS CONTEXT.

Each BBQ sample's input is "Context: ... Question: ...". Ambiguous samples (context_condition ==
"ambig") use the ambiguous context directly. Every disambiguated sample's context starts with an
ambiguous context, and is assigned to it (longest matching prefix). Category and answer information
are deliberately NOT part of the key: blocks that differ only in the wording of the "unknown" option,
or that disambiguate the same scenario in opposite directions, belong to the same cluster.

Writes census/bbq_groups.csv with columns: sample_id, group_id, category, context_condition,
question_polarity, alt_key (category + ambiguous context + answer_info, for the sensitivity check).

    python census/bbq_groups.py            # needs inspect_evals installed (dataset downloads from HF)
"""
import csv, hashlib, json, os, re, warnings
warnings.filterwarnings("ignore")
from inspect_evals.bbq import bbq

ds = list(bbq().dataset)

def text(s):
    return s.input if isinstance(s.input, str) else " ".join(m.text for m in s.input)

def context(s):
    return re.search(r"Context:(.*?)Question:", text(s), re.S).group(1).strip()

ambiguous = {context(s) for s in ds if s.metadata["context_condition"] == "ambig"}

def ambiguous_context(s):
    c = context(s)
    if s.metadata["context_condition"] == "ambig":
        return c
    return next(c[:i].strip() for i in range(len(c), 20, -1) if c[:i].strip() in ambiguous)

h = lambda x: hashlib.sha1(x.encode()).hexdigest()[:12]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bbq_groups.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sample_id", "group_id", "category", "context_condition", "question_polarity", "alt_key"])
    for s in ds:
        a = ambiguous_context(s)
        alt = h(s.metadata["category"] + "|" + a + "|" + json.dumps(s.metadata["answer_info"], sort_keys=True))
        w.writerow([s.id, h(a), s.metadata["category"], s.metadata["context_condition"], s.metadata["question_polarity"], alt])
print(f"wrote {out}: {len(ds)} samples")
