# Clustered-uncertainty census v2: protocol (fixed before running)

**Question.** For each registered inspect_evals task that reports a standard error, is that standard
error computed over samples that are not independent?

**Pin.** inspect_evals `12d04e0`, inspect_ai 0.3.272. No model calls in stages 1–3.

**Unit.** A registered task (`registry_find(type=="task")`, 250 tasks), not a directory. v1 counted
directories, and that produced the fortress false positive.

**Stage 1: what each task reports (deterministic).** Construct the task with default arguments in a
subprocess (10-minute timeout, and abort if free disk falls below 20 GB). Record every metric attached
to its scorers and to the task, and flag `stderr` with and without `cluster=`. Tasks that fail to
construct are recorded with the reason (gated dataset, required argument, dependency, timeout). They
are NOT dropped.

**Stage 2: structure signals (deterministic, on the constructed dataset).**
- S1: for each scalar metadata key, the number of distinct values and the largest group size.
- S2: hashes of attached images and documents, with the count of distinct values.
- S3: a hash of the longest text block of 200+ characters in the input (a shared passage/context),
  with the count of distinct values.
- S4: sample-id prefixes (the id minus its last separator-delimited segment), with the count.
- S5: repeated identical input text across samples.

Also recorded: n samples and `epochs`.

**Stage 3: adjudication, by the lead reading the signals plus 3 example samples per flagged grouping.**
- **CLUSTERED:** a repeated grouping is a shared item, context, passage, image, puzzle, problem, or
  one factor of a crossed design, so outcomes can covary within it. The key and the evidence are
  recorded.
- **STRATA ONLY:** repeats are categories (subject, domain, difficulty, language, task family), each
  level containing many distinct items. Not a clustering problem.
- **INDEPENDENT:** no repeated grouping beyond strata.
- A task only matters here if it reports `stderr` (stage 1).

**False-negative control.** 10 tasks classed INDEPENDENT or STRATA ONLY, drawn at random
(seed 20260930), are re-checked by reading the dataset code.

**Quoting rule.** Only stage-3 CLUSTERED rows with stage-2 evidence are claims. Counts come from the
constructed dataset, never from code reading. Tasks that failed to construct are reported as "not
assessed", with the reason.

**Stage 4 (optional, costs money): effect size.** SE ratio on released per-sample results where they
exist. Otherwise a cheap-model run on a random subset of clusters (budget ≤ $5).
