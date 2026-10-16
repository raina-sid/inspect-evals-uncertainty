# Clustered-uncertainty census v2: results (2026-09-30)

Protocol: `PROTOCOL.md`, fixed before running. Pins: inspect_evals `12d04e0`, inspect_ai 0.3.272.
Scope: the first 170 of 250 registered tasks alphabetically (`abstention_bench` through `mind2web`).
The run was stopped by Sid after the disk guard fired; the remaining 80 tasks were not probed.

**Stage 1 (what is reported, from the constructed task's own metrics).**

| | tasks |
|---|---|
| probed | 170 |
| failed to construct (not assessed) | 44 |
| constructed | 126 |
| … report plain `stderr()` | **87** |
| … report `stderr(cluster=…)` | 3 (docvqa, drop, mgsm) |
| … report stderr only inside `grouped()` | 1 |
| … report no standard error | 35 |

**Stages 2–3 (the 87 plain-stderr tasks).**
- 49 were flagged by the deterministic signals (`stage3a_flags.json`).
- Every substantive flag was adjudicated from printed example groups, rebuilt from the datasets.

### CLUSTERED (21 tasks): plain stderr over non-independent samples

| task | what's shared | samples in shared groups | largest group | cluster key in metadata? |
|---|---|---|---|---|
| agentdojo | crossed user task × injection task | 1014/1014 | 15 / 42 | yes, but ids repeat across suites, so include `task_suite_name` |
| agie_lsat_rc | reading passage | 269/269 (40 passages) | 8 | no |
| agie_lsat_ar | logic-game setup | 230/230 (40 games) | 7 | no |
| agie_sat_en | reading passage | 206/206 (44 passages) | 7 | no |
| agie_logiqa_en | shared problem context | 130/651 | 5 | no |
| lingoly_too | problem sheet (+ obfuscated variants) | 1203/1203 (82 sheets) | 42 | yes, `overall_question_n` |
| infinite_bench_longbook_choice_eng | the book | 229/229 (58 books) | 4 | no |
| infinite_bench_code_debug | the repository | 390/394 (91 repos) | 6 | no |
| infinite_bench_longdialogue_qa_eng | the script | 143/200 | 4 | no |
| cyse4_malware_analysis | the malware report | 569/609 | 10 | yes, `sha256` |
| cyse3_visual_prompt_injection | identical prompt across different images (crossed) | 532/1000 | 14 | yes, `system_prompt` + `user_input_text` |
| cyse2_prompt_injection | test-case system prompt × injection variant | 161/250 | 48 | yes, `test_case_prompt` |
| bbq | scenario: ambiguous/disambiguated context × neg/non-neg question | 58,492/58,492 (14,102 scenarios) | 20 | no (`source_id` is a per-category row id) |
| macbench | the image | 758/1153 | 8 | no |
| boolq | the passage | 549/3270 | 9 | no |
| hellaswag | the source video | 2537/10042 | 10 | yes, `source_id` |
| lab_bench_figqa | the figure | 127/181 | 3 | no |
| lab_bench_dbqa | gene-set context | 109/520 | 7 | no |
| lab_bench_protocolqa | the protocol | 24/108 | 9 | no |
| frontier_cs_research | variants of one research problem | 26/39 (4 problems) | 12 | yes, `problem_id` |
| frontier_cs | the same research variants | 39/211 | 12 | yes, `problem_id` |

### Not claimed

- **Uncertain.**
  - agie_sat_en_without_passage: the same items as sat_en, with the passage removed.
  - commonsense_qa: questions sharing a source concept; weak.
  - gdm_sp03/04/08/09/12_milestones: milestones of one subtask, but n = 3–7, so an SE is uninformative
    either way.
- **Template or strata (shared instruction or few-shot prompt, or category levels).** bbh, mathvista,
  frontierscience, chembench, bfcl (also has cross-subset duplicate questions), compute_eval, gdpval,
  lab_bench_seqqa.
- **Negligible repeats, not examined individually.** arc_challenge, arc_easy, apps, agie_lsat_lr,
  agie_sat_math, math, mbpp, humaneval, agent_bench_os, gdm_in_house_ctf, gdm_intercode_ctf,
  agent_threat_bench_autonomy_hijack (n=6), frontier_cs_algorithmic.
- **Independent (no flag):** 38 tasks.

**False-negative control** (seed 20260930, 10 drawn from the unflagged, template and strata pool of
48). All 10 were re-checked: 0 missed clusters. One of them, lab_bench_tableqa, has 262 distinct images
across 244 samples, so none are shared.

**Known from v1, but outside the 170:**
- worldsense: 87,048 samples in 40,176 tuples, verified from data;
- vqa_rad: 451 questions over 203 images;
- zerobench_subquestions.

**Effect sizes:** see [`../effect-size/RESULTS.md`](../effect-size/RESULTS.md) (lingoly_too 2.89×, agie_lsat_rc 1.10×) and
[`../effect-size/agentdojo_oneway.py`](../effect-size/agentdojo_oneway.py) (AgentDojo 2.51–2.68× one-way).

_Corrected 2026-10-12: the BBQ row originally counted only contexts of 200+ characters (29,088). Grouping on the full scenario text (verified at `12d04e0`), every sample is clustered: 14,102 scenarios, each ambiguous context plus its disambiguations, max 20._

**BBQ grouping definition (added 2026-10-16).** The census key is the *ambiguous context*: it plus every
disambiguated context that extends it. That gives 14,102 groups (13,821 of size 4; the rest 8–20).
An alternative key, category + ambiguous context + answer information (proposed in
[#1](https://github.com/raina-sid/inspect-evals-uncertainty/issues/1)), gives 14,603 groups, splitting 281
of ours. In all 281, every item shares the same ambiguous context and the same two questions. In 271, the
ambiguous items in the split blocks are identical except for the wording of the "unknown" option
("Can't be determined" vs "Cannot be determined"). The blocks otherwise differ in the disambiguated sentence,
i.e. counterbalanced versions of one scenario. 2 groups span two categories. We use the context-level key
as the primary cluster and the finer key as a sensitivity check. The dataset has 78 exact duplicate rows
(identical input, choices, target and answer metadata), all included, because the inspect port evaluates them.
