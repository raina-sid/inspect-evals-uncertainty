# Effect-size check, pre-registered 2026-09-30

- **Model:** `openai/gpt-5.6-luna`, default settings, 1 epoch. Budget cap $3 in total, checked after a
  5-sample smoke run.
- **Tasks:**
  1. `inspect_evals/agie_lsat_rc`, all 269 samples. Cluster = the reading passage (hash of the input's
     longest ≥200-char block, which census v2 verified: 40 passages, 269/269 samples).
  2. `inspect_evals/lingoly_too`, all 1203 samples. Cluster = `metadata["overall_question_n"]` (82 sheets).
- **Measure:** the task's own headline metric, and its SE computed by inspect_ai's `stderr()` versus
  `stderr(cluster=<key>)` on the same SampleScores. Report ratio = clustered/plain.
- **No other analysis, and no reruns to "improve" a ratio.** Whatever comes out is reported.
