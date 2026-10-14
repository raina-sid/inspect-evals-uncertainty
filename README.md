# Uncertainty in Inspect Evals: are the error bars computed over independent samples?

Of the 126 Inspect Evals tasks we could build, 87 report a plain `stderr()`, which assumes every sample is independent. Many datasets
violate that: several questions share a passage, an image, a scenario or a problem sheet, or the design
is crossed (e.g. user task × injection task). In those cases the plain standard error is too small.
Point estimates are unchanged; only the stated uncertainty is wrong. This matters most for model
comparisons and sample-size decisions.

This repo is the working hub for that question. Discussion and the proposal live in
[inspect_evals#2605](https://github.com/UKGovernmentBEIS/inspect_evals/issues/2605); results get posted there.

## Workstreams

| workstream | who | status | where |
|---|---|---|---|
| Census: which tasks report plain `stderr()` over clustered samples | [@raina-sid](https://github.com/raina-sid) | done for 170/250 tasks | [`census/`](census/) |
| Effect sizes on real runs (lingoly_too, agie_lsat_rc, agentdojo one-way) | [@raina-sid](https://github.com/raina-sid) | done | [`effect-size/`](effect-size/) |
| AgentDojo: two-way clustering, pigeonhole bootstrap, coverage study | [@couldbeme](https://github.com/couldbeme) | done | [couldbeme/agentdojo-two-way](https://github.com/couldbeme/agentdojo-two-way) |
| cyse2 / cyse3 crossed designs | [@couldbeme](https://github.com/couldbeme) | planned | — |
| BBQ: shared-scenario structure and its effect on uncertainty | [@GBX-Max1220](https://github.com/GBX-Max1220) | in progress | [#1](https://github.com/raina-sid/inspect-evals-uncertainty/issues/1) |

Coordination happens in this repo's issues. Each person's work stays in whichever repo they prefer.

## Results so far

**Census** ([`census/RESULTS.md`](census/RESULTS.md)). Scope: the first 170 of 250 registered tasks,
alphabetically. 126 constructed; 87 report a plain `stderr()`; 21 are verified as clustered, each
confirmed against example groups in the built dataset. A check of 10 random "not clustered" tasks found
no missed clusters.

**Effect sizes** ([`effect-size/RESULTS.md`](effect-size/RESULTS.md)). Computed with inspect_ai's own
`stderr()` vs `stderr(cluster=…)` on the same scores:

| task | clustered / plain SE |
|---|---|
| lingoly_too | 2.89× |
| agentdojo, one-way (upstream released runs; [`agentdojo_oneway.py`](effect-size/agentdojo_oneway.py)) | 2.51–2.68× |
| agie_lsat_rc (model near ceiling) | 1.10× |

Two-way (CGM) on the same AgentDojo runs gives 2.71× (attack success) and 2.84× (utility) with the same script; couldbeme's repo covers all 28 pipelines plus coverage.

**Known limitation of the census signal.** Shared contexts were detected from text blocks of ≥200
characters. That undercounted BBQ, whose contexts are short; the corrected row is in the results. Other
short-context evals may be similarly undercounted.

## Reproducing

**Versions:** inspect_evals `12d04e0`, inspect_ai main `4833f2e` (reports itself as 0.3.272), Python 3.12.
The census needs no model calls; the effect-size runs used `openai/gpt-5.6-luna`.

```bash
# census, stages 1–2: construct every registered task and record its metrics and dataset structure
cd census
python run_all.py stage12.jsonl
# stage 3a: flag candidate clusters among the plain-stderr tasks
python flag.py            # reads stage12.jsonl, writes stage3a_flags.json
cd ..
# effect size on any .eval log (KEY = a metadata field, or 'passage')
python effect-size/se_ratio.py <log.eval> <KEY>
# AgentDojo one-way and two-way SE from the upstream released runs (agentdojo @ 089ed46)
python effect-size/agentdojo_oneway.py <agentdojo>/runs/claude-3-7-sonnet-20250219
```

The census protocol, with its definitions and quoting rules, is in [`census/PROTOCOL.md`](census/PROTOCOL.md).
Note: "v1" in these files refers to an earlier, code-reading pass that is not included here.

---

_AI assistance: code and docs were drafted with an AI coding assistant (Claude). Every figure is reproducible
with the scripts in this repo; the `.eval` logs of the gpt-5.6-luna runs are not included but are available on request._
