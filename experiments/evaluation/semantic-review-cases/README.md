# Semantic review benchmark — candidate labels (NOT evaluated)

These examples are **constructed from project-level requirements** to test generalization, not a catalog of one bug per test. They deliberately include:
- a minimal viable design (positive control);
- responsibility drift with a valid dependency graph;
- functional contract drift with valid architecture;
- unjustified complexity under KISS/YAGNI;
- conflicting authority requiring an uncertain verdict;
- one historical RPG witness.

Cases and expected outcomes are separate. They are **provisional annotations** written before model execution, NOT independent acceptance criteria yet. A human must adjudicate interpretations before this set is frozen.

## Protocol

For an evaluation, supply only ONE candidate file along with the versioned requirements/policy and review prompt. Keep the annotations outside the model's workspace (the repository alone is NOT a blinded environment). Collect the response through the evidence-based protocol and compare the reported assessments against the held-out labels.

Record false-positive BLOCK decisions on the minimal design and false-negative approvals on the drifted examples, as well as uncertainty and model usage/latency. Do not optimize a prompt against this same small visible sample and then report that sample as held-out.

[Report contract](../../../docs/engineering/semantic-review.md) governs provenance; [architecture policy](../../../docs/engineering/policy.md) governs design semantics.
