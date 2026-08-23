---
applyTo: "tests/**/*.py,tests/**/*.md"
excludeAgent: "coding-agent"
---

# Automation PR Review Instructions (Playwright + Django)

These instructions are for Copilot **code review** of automation pull requests under `tests/`.
Use this document together with `tests/AGENTS.md` and enforce repository standards rigorously.

## 1. Authority and Precedence

- Primary source of truth is `tests/AGENTS.md`.
- If this file conflicts with `tests/AGENTS.md`, `tests/AGENTS.md` wins.
- If contributor intent conflicts with framework constraints, framework constraints win.
- User or repository owner direct instruction has top priority.

## 2. Review Mission

The review must prioritize:

- functional correctness over style,
- framework consistency over local shortcuts,
- traceability from backend behavior to Page Object and tests,
- automation stability and non-flaky execution,
- regression safety for existing modules.

## 3. Mandatory Review Output Structure

Always return findings first, ordered by severity:

- `Blockers`
- `Important`
- `Nice-to-have`

Each finding must include:

- file and line reference,
- concrete risk,
- explicit actionable fix recommendation.

If no findings exist, state that explicitly and still report:

- residual risk,
- coverage gaps,
- any unexecuted validation steps.

## 4. Non-Negotiable Blocker Rules

Mark as `Blocker` if any of the following is true:

- module-specific fix implemented in protected parent classes without explicit authorization,
- backend assumptions used in tests without verifying backend source,
- custom logic introduced where vanilla framework methods can solve the scenario,
- selectors intentionally left ambiguous and likely to fail in strict mode,
- destructive rewrite of existing module tests/page when extension was sufficient,
- missing evidence of required validation execution for high-impact changes.

## 5. Parent Class Protection and Authorization Policy

The following files are protected:

- `tests/pages/core/base_page.py`
- `tests/pages/core/standard_django_page.py`
- `tests/pages/core/generic_page.py`
- `tests/pages/core/fields_page.py`
- `tests/pages/core/constants.py`
- `tests/pages/core/mixins/*`

Any modification to these files is allowed **only with explicit owner authorization**.

For review acceptance when parent classes are modified:

- confirm authorization is explicitly documented in PR description or linked discussion,
- confirm why child/module-level customization was insufficient,
- confirm change is global (not single-module patch),
- require extended regression execution before approval.

If authorization is missing, reject as `Blocker`.

## 6. High-Risk Change Classification

Treat PR as high-risk if it modifies any of:

- protected parent classes or mixins,
- selector resolution behavior in shared layers,
- dependency resolution flow,
- formset core handling,
- global constants used by automation framework,
- data generation strategy factories,
- global validation flow.

High-risk PRs require broader regression checks, not only module-local execution.

## 7. Regression Execution Policy for Risky Changes

If there is potential to break other tests, review must require running additional suites.

Minimum required execution by risk level:

- low risk: changed module only.
- medium risk: changed module + one dependent module + one unrelated representative module.
- high risk: changed module + multiple representative modules + smoke subset.

Recommended execution commands:

- `cd tests`
- activate `tests/venv`
- `python -m pytest e2e/<domain>/test_<module>.py -s -v`
- `python -m pytest -k "<PREFIX>_" -s -v`
- `python -m pytest e2e -m smoke -s -v`

If broad execution was skipped, PR must include an explicit limitation statement and risk note.

## 8. Mandatory Backend-to-Automation Traceability

For each automated module, reviewer must verify mapping against:

- `apps/<module>/models.py`
- `apps/<module>/forms.py`
- `apps/<module>/views.py`
- `apps/<module>/filters.py` if present
- `apps/<module>/consts.py` if present
- `apps/<module>/urls.py`

Confirm that Page Object modeling aligns with backend truth:

- field names and field types,
- required vs optional behavior,
- limits and constraints,
- filters and available filter fields,
- detail/index visibility,
- delete/disable/enable behavior,
- dependency/formset behavior.

Any unmapped backend rule should be raised as at least `Important`.

## 9. Page Object Contract Checks

Validate the module Page Object contains coherent configuration:

- proper enum naming (`Field<Module>Enum`),
- proper class naming (`Page<Module>`),
- correct `super().__init__` setup,
- coherent `module_name` and navigation path,
- selectors only when truly module-specific,
- explicit `delete_mode` when behavior differs,
- precise `input_field_instances` with relevant constraints only.

Reject overconfiguration noise and underconfiguration that causes false positives.

## 10. Override Coherence Policy (Mandatory)

When methods are overridden in module Pages or tests, reviewer must verify:

- override is necessary and justified,
- override behavior is aligned with backend and test intent,
- parent contract is respected (input/output/side effects),
- `super()` is used when extension is intended, not silent replacement,
- no duplicated parent logic without clear reason,
- no hidden behavior drift that can break other modules.

If override purpose is unclear or contradicts framework behavior, mark as `Blocker` or `Important` based on impact.

## 11. Vanilla-First Enforcement

Before accepting custom flows, ensure contributor attempted:

- existing generic mixin methods,
- `FieldsPage` configuration,
- dependency configuration,
- formset configuration.

Only then custom module-level methods are acceptable.

Reject custom code that bypasses vanilla capabilities without evidence.

## 12. Selector Quality and Strict-Mode Safety

Selector review rules:

- prefer deterministic selectors (title/text/role/semantic attributes),
- avoid broad class selectors unless guaranteed unique,
- keep selector customizations inside module Page class,
- do not place raw selectors in test methods unless unavoidable.

When strict-mode collisions are plausible, request immediate refinement.

## 13. Coverage Matrix Expectations

For applicable modules, expected coverage includes:

- create flow,
- validate record flow,
- edit flow,
- delete/disable flow,
- enable flow if supported,
- create invalid scenarios,
- edit invalid scenarios,
- create valid scenarios,
- edit valid scenarios,
- filter scenarios by relevant fields,
- no-results filters,
- clear filters,
- empty filters where implemented,
- cancel create,
- cancel edit,
- back button on create/edit/detail where available,
- cancel delete modal,
- cancel enable modal where available,
- edit without changes,
- formset row deletion where applicable,
- dependency scenarios where applicable.

Missing applicable categories without justification should be reported.

## 14. Field Visibility and Index/Detail Coherence

Ensure assertions match real UI rendering:

- if field is not in index, `is_indexable` should be false,
- if field is detail-only, assert in detail context, not index,
- if backend index keys differ from model field names, automation must align to rendered output.

Reject index assertions for fields that UI does not expose in index.

## 15. Dependency and Cleanup Safety

Review dependency cleanup behavior carefully:

- default path should clean dependencies safely,
- if `delete_dependencies=False` is used, ensure scenario-specific justification exists,
- ensure no orphan records are silently left without reason.

If cleanup strategy may leak state and contaminate other tests, mark as `Important` or `Blocker`.

## 16. Formset and Conditional Field Precision

When formsets/conditional fields are present:

- validate formset configuration integrity,
- validate required-row behavior,
- validate add/delete row logic,
- validate active/inactive conditional field behavior,
- avoid manual row handling if framework mixins already support it.

## 17. Data Generation and Validation Strategy Checks

Verify contributor used framework constants/enums/utilities:

- `ValidDataType`, `InvalidDataType`, `InputType`, `DependencyAction`, `DeleteModeEnum`,
- existing data generation factories and helpers.

Avoid accepting PRs that introduce ad hoc random builders for module-local needs already solved by framework utilities.

## 18. Flakiness Prevention Rules

Reviewer should flag:

- arbitrary sleeps where deterministic waits are available,
- brittle selectors tied to layout-only CSS classes,
- test interdependence between cases,
- hidden environment assumptions not documented.

If risk is real, request stabilization before approval.

## 19. Naming and ID Consistency

Validate:

- file naming conventions (`page_<module>.py`, `test_<module>.py`),
- enum/class naming conventions,
- stable and unique case IDs (`<PREFIX>_<NN> <purpose>`),
- no accidental renumbering that harms traceability.

## 20. Evidence Requirements

PR should provide execution evidence appropriate to scope:

- module test run output,
- additional regression runs when risk requires,
- explicit report of pass/fail and any skipped coverage.

If evidence is missing for substantial changes, request it before approval.

## 21. Review Decision Rubric

Recommend `Approve` only when:

- no blockers,
- architecture and standards are respected,
- coverage is adequate for scope,
- validation evidence is sufficient for risk level.

Recommend `Changes requested` when:

- any blocker exists,
- risky change lacks required regression proof,
- overrides or custom code are unjustified,
- parent-class changes lack explicit authorization.

## 22. Final Principle

Automation PR quality in this repository means:

- backend truth first,
- configuration-driven implementation first,
- custom code only when truly necessary,
- protected parent classes changed only with explicit owner authorization,
- proactive regression protection for the broader test suite,
- clear, deterministic, maintainable module automation.
