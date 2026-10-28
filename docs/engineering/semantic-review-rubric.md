# Semantic engineering rubric

Use one pass/fail/uncertain assessment **per requested rule** and anchor each claim in source lines. Do not invent requirements or automatically modify accepted artifacts.

| Rule | Question |
| --- | --- |
| AR-01 | Does Domain own business policy, Application use cases, and outer adapters I/O? |
| AR-02 | Are dependencies inward, avoiding infrastructure in policy? |
| AR-03 | Is the responsibility assigned to the right accepted layer independently of a file name? |
| SOLID-S | Are modules cohesive with clear responsibilities? |
| SOLID-D | Does high-level policy avoid coupling to concrete adapters? |
| KISS | Is there a materially simpler way to meet the same accepted requirements? |
| YAGNI | Do added abstractions and features have a current requirement or accepted operational justification? |
| SPEC-TRACE | Does the proposal preserve every relevant accepted functional requirement? |

Missing acceptance evidence should be marked uncertain, not pass or fail. A model may propose a review, never accept architecture.
