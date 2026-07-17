# Evaluation fixtures for the legal writing skills

This directory holds fixtures, not results. `triggering.json` and `output-quality.json` are inputs to be run against a real model with the three skills installed. Nothing in this repository has executed them against a model, and nothing here should be read as a claim that `formal-legal-voice`, `prof-legal-voice`, or `informal-legal-voice` have passed a model evaluation. Static JSON validity is the only thing that has been checked mechanically; every check that requires a model call is described below as a procedure the maintainer must run and record separately.

## What the two files contain

`triggering.json` is a list of cases with the fields `id`, `prompt`, `expected_skill`, `must_not_select`, and `reason` (some cases carry an additional `category` field: `positive-trigger`, `non-trigger`, `boundary`, or `express-invocation`, to make the counts in this README auditable). `expected_skill` is `null` for the handful of cases where no legal writing skill should activate at all.

`output-quality.json` is a list of source-grounded drafting tasks with the fields `id`, `skill`, `task`, `source_facts`, and `rubric`. Every fact in `source_facts` is complete and fictional; none of them contain a placeholder such as `[date]` or `TBC`. The rubric is a set of pass/fail or short-answer checks a reviewer applies to the model's output; it is not itself a scoring script.

## Triggering accuracy

Run every prompt in `triggering.json` against the model, with only the skill discovery metadata available (that is, before any skill's body has been loaded), and record which skill, if any, activates. A pass means the activated skill equals `expected_skill` and none of the skills listed in `must_not_select` activated. Report the pass rate by category (`positive-trigger`, `non-trigger`, `boundary`, `express-invocation`) separately, because a drop in accuracy on ambiguous or boundary cases is a different and more instructive failure than a drop on the clear cases.

## Isolation testing

Test each skill installed on its own, with the other two absent, before testing them together. Isolation testing checks that a skill's own description is specific enough to fire on the prompts meant for it and stay silent on the prompts meant for another register, without another skill's presence acting as a foil. Run the full `positive-trigger` and `non-trigger` subsets for each skill in isolation.

## Coexistence testing

Reinstall all three skills together and rerun the full `triggering.json` file. Coexistence testing is where competing triggers surface: two skills judged individually plausible for the same prompt, or a skill activating alongside another when only one should. Compare the coexistence results against the isolation results for the same prompts; any prompt that passed in isolation but fails once all three are installed is a routing conflict, not a content defect, and should be fixed in the router section of the affected `SKILL.md` files rather than in the body text.

## Instruction-following testing

Instruction-following testing checks that once the correct skill has activated, it actually follows the skill's own workflow: the classify-source-draft-audit sequence, the document-function-specific ordering (for example, a file note using the neutral record structure rather than advocacy), and the source boundary (asking one focused question for a missing essential fact rather than inventing it, per the `output-quality.json` cases built around a missing deadline). This is distinct from triggering accuracy: a case can trigger the right skill and still fail instruction-following if the draft ignores the workflow.

## Output-quality testing

Run each task in `output-quality.json` against the named skill and score the output against its rubric. Because the rubric fields are a mix of booleans and short factual answers (an exact amount, an exact date, a retained defined term or quotation), scoring should be done by a reviewer reading the output against the source facts, not by keyword matching alone; a model can satisfy a keyword check while still inventing a fact or silently changing an amount. Record every rubric field individually rather than a single pass or fail per case, so a partial failure (for example, the deadline is preserved but an unsupported reassurance is added) is visible in the record.

## Testing on each deployed model tier

Trigger reliability and instruction-following are not guaranteed to transfer across model tiers. Run both files against every model tier the skills are actually intended to run on (for example, whichever tiers are enabled in the relevant Claude product or API configuration), and keep the results separate by tier. A skill that triggers reliably and follows the workflow on a larger model but not a smaller one is a real finding, and the fix may be a sharper description or a shorter body rather than a content change, since smaller tiers are typically more sensitive to length and ambiguity in the discovery metadata.

## Recording failures before changing instructions

Before editing any `SKILL.md`, `references/register-guide.md`, or `examples.md` in response to a failure, record the failing case id, the model tier, the actual output, and the specific rubric or routing field that failed. Do not edit the skill from memory of "it seemed to get this wrong sometimes." A change made without a recorded failure cannot be checked for regression, and a change made to fix one case can silently break another; the fixture files exist so that every change can be rerun against the full set, not just the case that prompted it. Keep the recorded failures alongside the fixture files (for example, in a dated results file outside this directory) so that a fix can be verified against the same case that motivated it, and so that a later regression shows up as a case that used to pass and no longer does.

## What is not claimed here

No model evaluation has been run against these fixtures as part of producing this directory. The counts below describe the fixtures themselves, not a pass rate:

- `triggering.json`: 42 cases (15 positive triggers, 9 non-triggers, 13 boundary or ambiguous cases, 5 express-invocation cases).
- `output-quality.json`: 19 source-grounded tasks (7 for `formal-legal-voice`, 6 for `prof-legal-voice`, 6 for `informal-legal-voice`).

Both files are valid JSON, checked by loading them with Python's standard library `json` module. Running the model-based procedures above, and recording the results, is separate work that has not been done as part of creating these fixtures.
