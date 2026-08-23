# AGENTS.md - Playwright E2E Automation Standard (Scope: `tests/`)

This file defines the mandatory agent behavior for everything under `tests/`.
It is intentionally strict and extensive to keep automation work consistent, scalable, and reusable.

## 1. Scope and Precedence

- This standard applies to all files inside `tests/`.
- User direct instructions always take top priority.
- If there is a conflict between style preferences and framework constraints, framework constraints win.
- This document is execution-oriented: it defines how to implement and extend automation, not just how to describe it.

## 2. Canonical Knowledge Sources Used to Build This Standard

The following documentation was considered as baseline for this English standard:

- `Playwright Automation.md`
- `Framework.md`
- `Introduction to Playwright and Automation.md`
- `Project Set Up and Configuration.md`
- `Framework/1. Arquitectura del Framework.md`
- `Framework/2. BasePage.md`
- `Framework/3. StandardDjangoPage.md`
- `Framework/4. HelpersMixin.md`
- `Framework/5. NavigationMixin.md`
- `Framework/6. ValidationMixin.md`
- `Framework/7. FormsetMixin.md`
- `Framework/8. GenericPage.md`
- `Framework/9. FieldsPage.md`
- `Framework/10. Crear Page Objects.md`
- `Framework/11. Patrones Comunes.md`
- `Framework/12. Utils Functions.md`
- `Framework/13. Estructura de Archivos de Tests.md`
- `Framework/14. Glosario de Metodos - Page Objects.md`
- `Framework/15. Constants (Constantes y Enumeraciones).md`

## 3. Main Objective

When a user says:

- `create tests for module X`
- `automate module X`
- `complete test coverage for X`

the agent must execute a complete module workflow:

- Inspect backend sources first (`forms`, `models`, `views`, `filters`, `consts`, `urls`).
- Build or extend the module Page Object.
- Build or extend module E2E tests.
- Reuse framework vanilla capabilities first.
- Keep custom code to an absolute minimum.
- Never modify parent/base framework classes for module-specific behavior.

## 4. Non-Negotiable Constraints

- Do not modify framework parent classes:
- `tests/pages/core/base_page.py`
- `tests/pages/core/standard_django_page.py`
- `tests/pages/core/generic_page.py`
- `tests/pages/core/fields_page.py`
- `tests/pages/core/constants.py`
- `tests/pages/core/mixins/*`
- If a page or test file already exists, do not rebuild from scratch.
- Complement existing coverage, preserve existing intent, and avoid destructive rewrites.
- Do not add one-off global helpers for a single module if the same can be solved in the module Page class.
- Keep the framework style and conventions already used in this repository.

## 5. Personal Rules Requested by Project Owner (Mandatory)

These are explicit owner requirements and must always be respected:

- Before implementing tests for any module, inspect backend definitions:
- `forms.py` to identify actual form fields and form-level validations.
- `views.py` to identify behavior, flows, permissions, titles, disable/enable mode, and endpoints.
- `models.py` to identify constraints, field types, and domain validations.
- Build the Page Object as complete as possible for that module.
- If tests already exist, do not start from zero; extend and complement them.
- Parent classes are protected and must not be edited.
- If custom behavior is needed, override or add methods only in each module Page class.
- Target `0 custom lines` in Pages and tests when framework vanilla configuration can solve the need.

## 6. Mandatory "First Reply" Behavior Before Coding

When user asks for a specific module automation:

- Start by confirming the execution approach in one concise message.
- Explain that backend files will be inspected first.
- Explain that existing Page/Test files will be complemented instead of recreated.
- Then execute implementation immediately.

## 7. Required End-to-End Module Workflow

Follow this exact sequence for every module task.

1. Module discovery in backend.
2. Existing automation discovery in `tests/pages` and `tests/e2e`.
3. Gap analysis (what exists vs what is missing).
4. Page Object extension or creation.
5. Tests extension or creation.
6. Local validation run for touched module.
7. Clear report of what was added and what remains out of scope.

## 8. Backend Discovery Checklist (Always Execute)

For target module `apps/<module>/`, read:

- `models.py`
- `forms.py`
- `filters.py` if present
- `views.py`
- `consts.py` if present
- `urls.py`

Extract and track:

- Field types and names.
- `max_length`, `min_length`, `choices`, `blank`, `null`, `default`, `unique`.
- Form `clean_*` and custom validation logic.
- Which fields are shown in index and detail.
- Which fields are filterable.
- Disable/enable/delete behavior.
- Modal and success/error message behavior.
- Any dependency relationship (FK, M2M, conditional dependencies).
- Formset usage and row behavior.

## 9. Existing Automation Discovery Checklist

Search and inspect:

- `tests/pages/**/page_<module>.py`
- `tests/e2e/**/test_<module>.py`

Classify what already exists:

- CRUD tests.
- Invalid data tests.
- Valid data tests.
- Filters tests.
- Navigation/cancel/modal tests.
- Formset tests.
- Dependency tests.
- Regression/smoke tests.

Only implement missing or weak areas.

## 10. Traceability Matrix Rule (Backend -> Page -> Test)

Before coding, build an internal matrix for each field:

- Backend source definition.
- `FieldsPage` configuration.
- Test cases that validate the field in create/edit/filter/detail/index contexts.

Do not proceed to implementation if this mapping is incomplete.

## 11. Page Object Standard

File naming:

- `tests/pages/<domain>/page_<module>.py`

Structure baseline:

- Enum for fields: `Field<Module>Enum`.
- Class: `Page<Module>(GenericPage)`.
- `input_field_instances`.
- `input_field_dependencies` when needed.
- `formset_fields` when needed.
- `delete_mode` when needed.

### 11.1 Selector policy

- Prefer default selectors from framework unless module UI differs.
- Override only selectors that are truly module-specific.
- Keep selectors in Page class, not in tests.

### 11.2 Page customization policy

- Allowed: add methods only in `Page<Module>` for module-specific flow.
- Not allowed: change parent classes for a single module problem.
- If a custom Page method is added, keep it focused and reusable.

## 12. FieldsPage Modeling Rules

For each field, configure only what is required for correctness.

Primary parameters:

- `name`
- `field_selector` when default is insufficient
- `filter_selector` when default is insufficient
- `input_type`
- `filter_type` if filter input differs
- `is_required`
- `is_filter`
- `is_data_validate`
- `is_indexable`
- `is_editable`
- `max_length`
- `min_length`
- `min_value`
- `max_value`
- `allowed_values`
- `prioritized_values`
- `priority_percentage`
- `regex_pattern` and `regex_flags` for regex fields
- date/time format parameters only when module behavior requires it

### 12.1 Type mapping guideline

- Text-like fields -> `InputType.TEXT` or `InputType.TEXTAREA`
- Integer-like fields -> `InputType.NUMBER`
- Decimal-like fields -> `InputType.DECIMAL`
- Email -> `InputType.EMAIL`
- Date -> `InputType.DATE`
- Time -> `InputType.TIME`
- Datetime -> `InputType.DATE_TIME`
- Date ranges -> `InputType.RANGE_OF_DATES`
- Standard select -> `InputType.SELECT`
- Select2 single -> `InputType.SELECT2`
- Select2 multiple -> `InputType.SELECT2_MULTIPLE`
- File/Image -> `InputType.FILE`
- Pattern-constrained text -> `InputType.REGEX`

## 13. Dependencies Standard

Use `input_field_dependencies` with `DependencyAction`:

- `CREATE`
- `VALIDATE`
- `FILTER`
- `INDEX`

Guidelines:

- Keep value formatting config explicit.
- Reuse dependency Page Objects.
- Let `GenericPage` dependency flow handle data population whenever possible.
- For conditional dependent fields, configure `is_dependent`, `activating_field`, `activating_values`.

## 14. Formset Standard

When module uses formsets:

- Define `formset_fields` with explicit `add_button_selector`, `prefix_validate`, `is_required`, and row fields.
- Use vanilla formset support from mixin first:
- `generate_formset_data`
- `fill_formsets`
- `delete_formset_rows`
- `validate_delete_formset_row_on_create`
- `validate_delete_formset_row_on_edit`

Do not implement manual row handling unless framework behavior is insufficient for that module.

## 15. Vanilla-First Decision Tree

Always follow this decision order:

1. Use existing framework method as-is.
2. Solve by `FieldsPage` configuration.
3. Solve by dependency configuration.
4. Solve by formset configuration.
5. Add custom method in module Page class only.

Do not skip directly to custom logic.

## 16. Test File Standard

File naming:

- `tests/e2e/<domain>/test_<module>.py`

Expected structure:

1. Imports.
2. Parametrized credentials and case IDs.
3. CRUD baseline tests.
4. Invalid create tests.
5. Invalid edit tests.
6. Valid data tests.
7. Filters tests.
8. Navigation/cancel/modal tests.
9. Formset/dependency tests.
10. Smoke/regression tests.

## 17. Mandatory Test Coverage (Minimum Baseline)

For each module, include as many as applicable:

- Create record.
- Validate record.
- Edit record.
- Delete/disable record.
- Enable record if module supports it.
- Required field validation on create.
- Required field validation on edit.
- Max length validation.
- Min length validation when applicable.
- Min/Max numeric validation when applicable.
- Duplicate validation when applicable.
- Data type validation (email, regex, file format, etc) when applicable.
- Valid data creation scenarios.
- Valid data edition scenarios.
- Filter by each relevant filterable field.
- Filter no-results scenarios.
- Clear filters behavior.
- Cancel create behavior.
- Cancel edit behavior.
- Back button behavior (create/edit/detail) when applicable.
- Cancel delete modal behavior.
- Cancel enable modal behavior when applicable.
- Edit without changes behavior when applicable.
- Formset row deletion on create/edit when applicable.
- For `DeleteModeEnum.DISABLE_INDEX`: back button behavior on disabled index.
- For `DeleteModeEnum.DISABLE_INDEX`: no-results filter behavior on disabled index.
- For `DeleteModeEnum.DISABLE_INDEX`: clear-filters behavior on disabled index.
- For `DeleteModeEnum.DISABLE_INDEX`: empty-filters behavior on disabled index.

## 18. Preferred Vanilla Methods in Tests

Use these methods before writing custom test flow:

- `create_record`
- `edit_record`
- `delete_record`
- `enable_record`
- `validate_record`
- `validate_create_invalid_data`
- `validate_edit_invalid_data`
- `validate_create_valid_data`
- `validate_edit_valid_data`
- `filter_by_specific_field`
- `validate_no_results_on_filters`
- `validate_cancel_create_form_returns_to_index`
- `validate_cancel_edit_form_returns_to_index`
- `validate_back_button_on_create`
- `validate_back_button_on_edit`
- `validate_back_button_on_detail`
- `validate_back_button_on_disabled_index`
- `validate_clear_filters_button`
- `validate_clear_filters_button_in_disabled_index`
- `validate_empty_filters`
- `validate_no_results_on_filters(disabled_index=True)`
- `validate_empty_filters(disabled_index=True)`
- `validate_cancel_delete_modal`
- `validate_cancel_enable_modal`
- `validate_edit_without_changes`
- `validate_delete_formset_row_on_create`
- `validate_delete_formset_row_on_edit`

## 19. Constants and Enumerations Usage Rule

Prefer framework enums and constants instead of hardcoded literals:

- `ValidDataType`
- `InvalidDataType`
- `AllowedDatesFormates`
- `InputType`
- `DependencyAction`
- `DeleteModeEnum`
- `RegexFlag`
- Field and formset references in tests must use module enums (`Field<Module>Enum`, `Field<Module>FormsetEnum`) instead of string literals.
- Never pass hardcoded field names like `"quantity"` or `"nombre"` in `pytest.param` or `validate_*` / `filter_*` calls when an enum exists.

## 20. Data Generation Rule

Prefer existing utilities from framework utils rather than custom random builders:

- random strings/numbers/floats
- special chars
- email/phone/url/ip/mac
- regex-driven values
- date/time format helpers
- file/image generators

Only add new utility function when there is clear repeated use across modules.

## 21. Naming and IDs Convention

- Field enum: `Field<Module>Enum`
- Page class: `Page<Module>`
- Test IDs: `<PREFIX>_<NN> <clear purpose>`
- Keep IDs unique and stable.
- If existing numbering exists, continue from current sequence.

## 22. "Complement, Do Not Rebuild" Policy

If files already exist:

- Keep existing tests and add missing cases.
- Preserve working behavior.
- Avoid mass refactors unless explicitly requested.
- Do not erase user-specific custom flows without explicit approval.

If legacy commented blocks exist:

- Do not blindly uncomment all.
- Migrate only necessary stable scenarios.

## 23. Customization Boundary

Custom code is allowed only here:

- In module-specific Page class.
- In module-specific test file.

Custom code is not allowed here for module-specific fixes:

- Core base classes.
- Core mixins.
- Shared framework constants unless change is truly global and explicitly requested.

## 24. Quality Gate Before Completion

At minimum run module-level tests after edits, for example:

- `pytest tests/e2e/<domain>/test_<module>.py -s -v`
- `pytest -k "<PREFIX>_" -s -v`

If scope is broader, run broader suites accordingly.

If tests are not run, explicitly report that and why.

## 25. Definition of Done (DoD)

A module automation task is complete only if:

- Backend analysis was performed (`forms`, `views`, `models`, and related files).
- Page model reflects actual module behavior.
- Existing tests were complemented (or new ones created when absent).
- Coverage includes CRUD + validations + filters + module-specific flows.
- No forbidden parent-class modification was made.
- Validation commands were executed or limitation was clearly reported.

## 26. Anti-Patterns (Explicitly Forbidden)

- Writing tests before reading backend source.
- Assuming validations without checking backend files.
- Duplicating existing tests with only different IDs.
- Editing `GenericPage` or mixins to fix a single module edge case.
- Hardcoding random test data that framework generators already support.
- Over-customizing when vanilla configuration can solve it.
- Recreating entire Page/Test files when extension is enough.

## 27. Communication Rule During Module Tasks

During execution, keep user informed with concise progress:

- state that backend discovery is in progress
- state that existing page/test discovery is in progress
- state what will be edited before editing
- report validation run status

At completion, provide:

- what changed
- where it changed
- what was validated
- remaining risks or next steps

## 28. Quick Execution Blueprint

Use this mental template for every module:

1. Read backend files.
2. Read existing page and tests.
3. Build field/dependency/formset traceability.
4. Extend page with vanilla config first.
5. Extend tests with missing scenarios.
6. Keep parent classes untouched.
7. Run module tests.
8. Report concrete outcome.

## 29. Final Principle

This automation framework is configuration-driven.
The default strategy is always:

- maximum reuse
- minimum custom code
- no parent class modification
- complete module coverage based on backend truth

## 30. Required Intake Template (Use Before Any Module Work)

Before implementing module automation, the agent must internally fill this intake template:

- `Module name:` exact app/page domain requested.
- `App path:` `apps/<module>/`.
- `Page path:` existing or target path in `tests/pages/<domain>/page_<module>.py`.
- `Test path:` existing or target path in `tests/e2e/<domain>/test_<module>.py`.
- `Delete mode expected:` `DEFAULT`, `TOGGLE`, or `DISABLE_INDEX`.
- `Formset present:` yes/no.
- `Dependencies present:` yes/no.
- `Conditional fields present:` yes/no.
- `Generated fields present:` yes/no.
- `File/image fields present:` yes/no.
- `Regex fields present:` yes/no.
- `Special date formats present:` yes/no.

If any field above is unknown, backend discovery is incomplete.

## 31. Backend-to-Automation Mapping Table (Mandatory)

For every backend field, create an internal mapping row with:

- `field_name`
- `model_field_type`
- `form_widget_type`
- `required?`
- `validators`
- `choices`
- `unique?`
- `index_visible?`
- `detail_visible?`
- `filterable?`
- `page_input_type`
- `fields_page_config`
- `create_invalid_cases`
- `edit_invalid_cases`
- `valid_cases`
- `filter_cases`

The agent must not skip fields silently.
If a field is intentionally excluded, the reason must be explicit.

## 32. Exclusion Rules for Fields (When Not to Automate)

A field can be excluded from active validation only if one of these is true:

- backend marks it as generated and user does not require deep generated validation.
- internal/system field not shown in UI.
- field exists in model but is not exposed in the current form/view scope.
- field is hidden behind feature toggle unavailable in environment.

Each exclusion requires a documented reason in final report.

## 33. Extended Page Object Build Checklist

When creating or extending `Page<Module>`, verify:

- module_name is set correctly.
- navigation path reflects actual menu hierarchy.
- page titles are aligned with real UI text.
- create/edit/detail/index selectors are compatible with current UI.
- input field enum values exactly match backend field names.
- each `FieldsPage` has correct type and constraints.
- `is_filter`, `is_indexable`, `is_data_validate`, `is_editable` flags are coherent.
- dependencies map covers create/validate/filter/index when needed.
- formsets include row selector strategy and validation prefix.
- delete mode aligns with backend behavior.
- generated fields are explicitly declared when present.

## 34. Extended Test Coverage Matrix by Field Nature

### 34.1 Text fields

- required on create
- required on edit
- max_length
- min_length (if enforced)
- valid letters
- valid special chars if allowed
- duplicates if unique

### 34.2 Numeric/decimal fields

- required
- min_value
- max_value
- negative validation (if disallowed)
- decimal precision behavior (when applicable)

### 34.3 Select/Select2 fields

- required
- valid option selection
- invalid option handling when applicable
- filter behavior
- dependency injection behavior

### 34.4 Date/time/range fields

- required
- accepted format
- invalid format
- range consistency (start <= end)
- index/detail format expectations when custom formats apply

### 34.5 File/image fields

- valid format
- invalid format
- file size/weight limit if backend enforces it
- display/preview behavior if relevant

### 34.6 Regex-constrained fields

- valid pattern match
- invalid pattern rejection
- boundary cases for min/max length with regex

## 35. Scenario Taxonomy (Use This Naming Internally)

Every new test scenario should fit one of these categories:

- `CRUD_CORE`
- `INVALID_CREATE`
- `INVALID_EDIT`
- `VALID_CREATE`
- `VALID_EDIT`
- `FILTER_SINGLE`
- `FILTER_MULTI`
- `FILTER_NO_RESULTS`
- `FILTER_CLEAR`
- `NAV_CANCEL`
- `NAV_BACK`
- `MODAL_CANCEL`
- `STATE_ENABLE_DISABLE`
- `FORMSET_CREATE`
- `FORMSET_EDIT`
- `FORMSET_DELETE_ROW`
- `DEPENDENCY_CREATE`
- `DEPENDENCY_VALIDATE`
- `GENERATED_FIELD`
- `SMOKE`
- `REGRESSION`

This keeps large files readable and prevents blind duplication.

## 36. Stable Test ID Policy

- Never rename existing IDs unless explicitly requested.
- Never reuse an existing ID for a different behavior.
- New IDs must continue the module sequence.
- Keep ID prefix short and module-specific.
- ID text must include expected outcome, not only action.

## 37. Strong Rule for Existing Files

If `page_<module>.py` and `test_<module>.py` already exist:

- preserve original behavior and style.
- add missing validations and scenarios.
- avoid deleting tested flows unless they are broken by design and replaced.
- avoid formatting-only bulk changes in same patch as logic changes.

## 38. Allowed Customization Zones (Detailed)

Allowed:

- new methods in module Page class.
- new helper methods in module test file scoped to that file.
- selector overrides in module Page class.
- module-specific fixtures only if strictly required and local.

Not allowed:

- adding module-specific logic in shared core classes.
- changing strategy factories for one-off module behavior.
- changing global constants to satisfy a single test.
- introducing environment hacks in `conftest.py` for one module.

## 39. Parent Class Protection Contract

For module automation tasks, all the following are read-only unless user explicitly asks global framework refactor:

- `tests/pages/core/base_page.py`
- `tests/pages/core/standard_django_page.py`
- `tests/pages/core/generic_page.py`
- `tests/pages/core/fields_page.py`
- `tests/pages/core/constants.py`
- `tests/pages/core/mixins/helpers_mixin.py`
- `tests/pages/core/mixins/navigation_mixin.py`
- `tests/pages/core/mixins/validation_mixin.py`
- `tests/pages/core/mixins/formset_mixin.py`

## 40. Formset Precision Rules

When a formset exists:

- explicitly set `has_initial_row` if behavior is known.
- define row field selectors with predictable indexing strategy.
- verify row add count equals requested count.
- include at least one row-deletion validation test.
- include required-field validation inside formset rows.
- if dependency fields exist inside formset, map them with dependency configuration.

## 41. Dependency Precision Rules

For dependency-driven fields:

- always define create mapping first.
- add validate/filter/index mapping when displayed format differs.
- keep separators explicit and intentional.
- test dependency cleanup through standard deletion flow.
- if dependency quantity is configurable, validate non-default quantity in at least one scenario.

## 42. Conditional Field Rules

For `is_dependent` fields:

- set `activating_field`.
- set `activating_values`.
- include at least one test where field is active.
- include at least one test where field is inactive and safely skipped.
- avoid manual branching in tests if generic generation already supports it.

## 43. Generated Field Rules

If module has generated fields:

- configure `is_generated_field=True`.
- validate presence after create.
- include filtering behavior if generated field is filterable.
- do not attempt to fill generated fields directly.

## 44. Select2 and Select2 Multiple Rules

For `SELECT2` and `SELECT2_MULTIPLE`:

- ensure selectors point to container or expected search input flow.
- verify create and edit flows.
- verify filter behavior where applicable.
- for multi-select dependency mode, validate concatenated display values.
- for table-rendered multi-select, configure `table_suffix` when needed.

## 45. Date/Time Rules

When custom format is used:

- set input format for fill behavior.
- set detail/index format for validation behavior.
- set separators explicitly if module differs from defaults.
- include at least one format-sensitive validation scenario.

## 46. File and Media Rules

When module uploads files:

- include valid file scenario.
- include invalid extension scenario.
- include size limit scenario if backend validates size.
- include cleanup-safe behavior in teardown path.

## 47. Regex Rules

For regex fields:

- set regex pattern in `FieldsPage`.
- set regex flags when needed.
- include both valid and invalid regex scenarios.
- keep pattern source aligned with backend validator, never guessed.

## 48. Filter Coverage Rules

For filters:

- cover at least one text filter.
- cover at least one non-text filter if available (select/date/etc).
- validate no-results behavior.
- validate clear-filters behavior.
- validate empty-filter baseline when implemented.
- if module uses `DeleteModeEnum.DISABLE_INDEX`, also validate no-results, clear-filters, and empty-filters in disabled index.

## 49. Navigation and Modal Rules

For navigation:

- cancel create returns index.
- cancel edit returns index.
- back behavior on create/edit/detail if available.
- if module uses `DeleteModeEnum.DISABLE_INDEX`, include back behavior on disabled index.

For modals:

- cancel delete modal.
- cancel enable modal where applicable.
- success modal validation for core CRUD flows.

## 50. Smoke and Regression Rules

Per module, maintain:

- one smoke flow covering critical create-validate-edit-delete chain.
- regression tests for known bugs when applicable.
- regression tests should be concise and tied to a specific failure pattern.

## 51. Refactoring Safety Rules

When touching large existing test files:

- do not reorder everything unnecessarily.
- avoid moving blocks unless required for clarity.
- keep git diff readable for review.
- isolate logical fixes from stylistic formatting.

## 52. Reporting Format at Task End

Final report should include:

- module analyzed.
- backend files inspected.
- page/test files modified.
- categories of scenarios added.
- tests executed and result summary.
- known gaps or blocked scenarios.

## 53. Command Cookbook (Recommended)

Module-level execution:

- `pytest tests/e2e/<domain>/test_<module>.py -s -v`

By case prefix:

- `pytest -k "<PREFIX>_" -s -v`

Smoke-level:

- `pytest tests/e2e -m smoke -s -v`

Debug logging:

- `pytest tests/e2e/<domain>/test_<module>.py -s -v --log-cli-level=DEBUG`

## 54. Failure Handling Protocol

If test fails:

1. classify failure: selector/data/validation/environment.
2. confirm backend expectation.
3. confirm page configuration.
4. confirm test expectation and fixtures.
5. fix at the narrowest valid layer.
6. rerun module-level suite.

Never apply broad framework-level changes for a single failing module unless explicitly approved.

## 55. Environment Safety Rules

- Respect `.env`-driven settings.
- Do not alter production/demo safety checks in test setup unless explicitly requested.
- Keep login and fixture usage aligned with existing `conftest.py`.
- Do not bypass auth flows with hidden shortcuts unless module design requires it.

## 56. Documentation-in-Code Rule

For new module Page methods:

- add concise docstring describing purpose and expected behavior.
- avoid excessive comments in obvious code.
- include comments only for non-trivial flow decisions.

## 57. Strict Duplicate Prevention

Before adding any new test:

- search existing module test file for same behavior.
- if equivalent case exists, improve existing case instead of duplicating.
- if adding variant, describe what makes it distinct.

## 58. Performance and Stability Rules

- prefer framework generators and helpers over arbitrary waits.
- avoid hard sleeps unless unavoidable.
- use selectors that are resilient across minor UI changes.
- avoid test interdependence; each case must be independently executable.

## 59. Suggested Module Test Block Template

Use this order in large files:

1. `CRUD CORE`
2. `INVALID CREATE`
3. `INVALID EDIT`
4. `VALID CREATE`
5. `VALID EDIT`
6. `FILTERS`
7. `NAVIGATION AND MODALS`
8. `FORMSETS`
9. `DEPENDENCIES`
10. `SMOKE`
11. `REGRESSION`

## 60. Suggested Page Object Template

At minimum:

- field enum
- page class with `super().__init__`
- module title selectors if required
- delete mode if required
- `input_field_instances`
- `input_field_dependencies` if required
- `formset_fields` if required
- optional focused custom methods

## 61. Cross-Check Against Framework Capabilities

Before writing any custom method, check whether one of these already solves the case:

- navigation mixin methods
- validation mixin methods
- formset mixin methods
- dependency handling in generic page
- field generation and validation in `FieldsPage`

If yes, custom method is unnecessary and should not be added.

## 62. Risk Register (Track During Work)

Track these risks for each module:

- selector fragility due dynamic UI.
- flaky date/time format expectations.
- dependency cleanup failures.
- formset row indexing drift.
- false positives in filter validation.

Mention remaining risks in final report when unresolved.

## 63. Escalation Rule

Escalate to user only when:

- business behavior is ambiguous in backend source.
- multiple valid automation interpretations exist.
- required data/permissions are unavailable.
- requested behavior would force forbidden parent class modification.

Otherwise proceed and implement.

## 64. Golden Rule

For this repository, module automation quality means:

- backend truth first
- complete page modeling
- complementary test growth
- vanilla-first implementation
- child-only customizations
- zero parent-class edits for module-specific needs

## 65. Custom Gate (Vanilla-First Enforcement)

Before adding any custom line in module Page or module test file, the agent must explicitly validate this gate:

1. Which existing vanilla method was attempted.
2. Why `FieldsPage` configuration was insufficient.
3. Why dependency/formset configuration was insufficient.
4. Why custom logic is the narrowest valid solution.

If any of these points is missing, custom implementation must not be added.

## 66. Mandatory Method Selection Matrix

Use this matrix before implementing a scenario:

- create base flow -> `create_record`
- edit base flow -> `edit_record`
- delete/disable flow -> `delete_record`
- enable flow -> `enable_record` or `validate_enable_record`
- create invalid data -> `validate_create_invalid_data`
- edit invalid data -> `validate_edit_invalid_data`
- create valid data -> `validate_create_valid_data`
- edit valid data -> `validate_edit_valid_data`
- filter by field -> `filter_by_specific_field`
- no results filter -> `validate_no_results_on_filters`
- no results filter on disabled index -> `validate_no_results_on_filters(disabled_index=True)`
- clear filters -> `validate_clear_filters_button`
- clear filters on disabled index -> `validate_clear_filters_button_in_disabled_index`
- empty filters -> `validate_empty_filters`
- empty filters on disabled index -> `validate_empty_filters(disabled_index=True)`
- cancel create -> `validate_cancel_create_form_returns_to_index`
- cancel edit -> `validate_cancel_edit_form_returns_to_index`
- back create/edit/detail -> `validate_back_button_on_create` / `validate_back_button_on_edit` / `validate_back_button_on_detail`
- back disabled index -> `validate_back_button_on_disabled_index`
- cancel delete modal -> `validate_cancel_delete_modal`
- cancel enable modal -> `validate_cancel_enable_modal`
- edit without changes -> `validate_edit_without_changes`

Only if no matrix method solves the scenario, custom flow is allowed.

## 67. Strict Selector Policy

Selectors must be deterministic and action-specific:

- prefer semantic selectors (title/text/role) over generic class selectors.
- avoid ambiguous selectors such as broad `.btn-danger`, `.btn-primary`, etc.
- if UI returns strict-mode collision, refine selector in module Page class only.
- never solve selector ambiguity by editing core framework classes for a single module.

## 68. Field Visibility Contract (Index vs Detail)

For each backend field, define visibility explicitly:

- if field is not rendered in index table -> set `is_indexable=False`.
- if field is rendered in detail only -> keep detail validation active.
- if field is filterable but not indexable -> keep `is_filter=True` and `is_indexable=False`.
- if backend `INDEX_FIELDS` differs from model/form naming, align Page config to actual UI rendering, not guessed field names.

Do not force index assertions for fields that UI does not render.

## 69. Dependency Cleanup Contract

When dependency cleanup causes unrelated instability, apply the narrowest safe cleanup strategy:

- prefer standard cleanup with dependency deletion.
- if module flow requires preserving dependency cleanup boundaries, allow `delete_dependencies=False` only at module test level.
- document why dependency cleanup is intentionally bypassed in that scenario.
- never patch parent cleanup logic for a single module issue.

## 70. Custom Method Template Rule

If custom method is unavoidable in `Page<Module>`:

- name with clear intent: `validate_<behavior>` or `<action>_<behavior>`.
- keep it single-responsibility.
- internally reuse existing mixin/generic helpers whenever possible.
- include concise docstring with: scenario objective, expected behavior, cleanup expectation.

Avoid long procedural custom methods when composition of existing methods is possible.

## 71. Execution Profiles Rule

Validation execution should follow these profiles:

- fast check (targeted): `pytest tests/e2e/<domain>/test_<module>.py -k "<CASE_ID>" -s -v`
- module full check (mandatory before completion): `pytest tests/e2e/<domain>/test_<module>.py -s -v`
- smoke check (optional when requested): `pytest tests/e2e -m smoke -s -v`

At task end, report exactly which profile(s) were executed.

## 72. Custom Scenario Admission Rule

A custom scenario is accepted only if at least one condition is true:

- regression for a known bug.
- module-specific UI behavior not covered by vanilla methods.
- business rule from backend cannot be expressed through current `FieldsPage` config.
- environment-specific behavior explicitly requested by user.

If none apply, scenario must be implemented with vanilla methods and configuration only.
