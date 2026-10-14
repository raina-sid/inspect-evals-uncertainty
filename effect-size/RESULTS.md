# Effect-size check: results (pre-registered in PREREG.md)

Model `openai/gpt-5.6-luna`, 1 epoch, inspect_evals `12d04e0`, inspect_ai main (editable). SE computed
by inspect_ai's own `stderr()` and `stderr(cluster=)` on the same SampleScores (`se_ratio.py`). In both
runs the plain SE equals the stderr the eval itself reports, which is a sanity check on the method.

| task | n | clusters | headline | plain SE | clustered SE | ratio | effective n |
|---|---|---|---|---|---|---|---|
| agie_lsat_rc (cluster = passage) | 269 | 40 | accuracy 0.937 | 0.0149 | 0.0164 | **1.10** | ~221 |
| lingoly_too (cluster = `overall_question_n`) | 1203 | 82 | original_mean 0.530 / obfuscated_mean 0.393 | 0.0114 | 0.0330 | **2.89** | ~144 |

For comparison, AgentDojo from its released runs: 2.51× (attack success, clustered by injection task)
and 2.68× (utility, clustered by user task).

**Reading.**
- The size of the correction depends on the cluster size and on how far the model is from ceiling.
  LSAT-RC with luna is at 94% with only 17 misses, so there's little room for errors to co-occur within
  a passage.
- lingoly_too has sheets of up to 42 items at mid-range accuracy, and 1,203 samples carry about as much
  information as 144 independent ones.

**Protocol note.** The lingoly_too run was stopped by the tool's 30-minute background limit at
1178/1203 samples. `inspect eval-retry` completed the remaining 25 on the same log, so all 1,203 are
included, as pre-registered. Tokens: lsat_rc 228k; lingoly_too 5.37M in total (mostly output and
reasoning).
