# Evaluation and rollback

Read when planning or testing improvements.

1. Identify the observed problem, evidence and a falsifiable change hypothesis. Distinguish observation from speculation.
2. Predefine representative tests, a baseline, relevant failure cases, a success threshold, and regression checks. Select metrics appropriate to the task: verified completion, correctness, retries, tool error rate, latency, cost, human correction or other grounded outcomes.
3. Preserve a diff or backup of the affected authorised files and state how to revert. Do not copy secrets or private logs into reports.
4. Apply the smallest reversible change feasible, avoiding simultaneous changes that confound the result.
5. Compare outcomes with the baseline, considering side effects, external variability, uncertainty, and cost. Seek independent or adversarial evaluation when worthwhile. A self-rating is not objective evidence.
6. Accept, revert, or gather more evidence based on results. Never redefine the criteria after seeing outcomes. Periodically test whether the improvement process itself has become counterproductive.

Capture the decision using `../assets/improvement-record.schema.json`. If measurement cannot be performed, report the result as inconclusive.
