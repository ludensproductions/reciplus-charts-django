# AGENTS.md

This document defines the operating rules for AI coding agents (e.g., GitHub Copilot) working in this repository.
The goal is to ensure that all generated code and reviews follow the team's standards: consistency, maintainability, and predictable architecture.

## 1. Role of the agent

You are an assistant to:
- implement code changes aligned with our architecture and conventions,
- propose improvements without introducing unrelated refactors,
- help during Code Review by identifying risks, inconsistencies, and missing tests/evidence.

You must **not**:
- introduce Function-Based Views (FBVs) in Django (strictly forbidden),
- add unrelated refactors or formatting-only changes unless explicitly requested,
- duplicate validation logic across layers (model/form/schema) without a strong reason,
- hardcode user-facing strings in the backend (must be centralized and translatable).

---

## 2. Default stack & assumptions

Unless the task explicitly states otherwise, assume the standard stack:
- Backend: **Python + Django**, APIs with **Django Ninja**
- DB: **PostgreSQL**
- Cache: **Redis**
- Async tasks: **Django-Q2** (default) or **RabbitMQ** when needed
- Frontend: **Django Templates + Vanilla JS + Bootstrap 5 template**, Font Awesome 6
- JS libs commonly used: **HTMX, Select2, Sweetalert2, Chart.js, DataTables**
- Containers: Docker/Podman; orchestration: Kubernetes
- CI/CD: Jenkins
- Testing: Playwright (pytest for Python) and/or Cypress; Security: OWASP ZAP; Performance: JMeter

---

## 3. Branching, PRs, and commit conventions

### 3.1 Branch naming
Use short-lived branches created from the main development branch (e.g., `dev` or `main` depending on the repo).

Recommended formats:
- `feature/<module>-<short-description>`
- `bugfix/<bug>`
- `hotfix/<bug>`
- `refactor/<module>`
- `automation/<module>`

Language for branch names may be Spanish or English, but must follow the prefix convention.

### 3.2 Pull Requests (PRs)
There are two common PR types:
1. **Development PRs (Backend/Frontend):** feature implementation, UI changes, Django code.
2. **Testing PRs (Automation):** Playwright/Cypress code and reports.

PR evidence requirements:
- If the PR affects **frontend UI**, include **screenshots or a GIF** of the flow.
- If the PR adds/changes **Playwright tests**, attach the **Playwright HTML Report** (and ideally a screenshot of the report).

### 3.3 Code Review workflow and “Ready for review”
A PR can move to “Ready for review” only after:
- it is reviewed and approved by the designated reviewer (architect/senior/tech lead),
- required evidence is attached (screenshots/GIF/report) when applicable.

### 3.4 Conventional Commits
Commit messages should follow Conventional Commits (English recommended):
- `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
Optionally add scope: `feat(login): ...`

---

## 4. Project structure expectations (Django)

Follow the standard Django structure:
- `apps/` contains all Django apps
- `djangoproject/` contains settings/urls/asgi/wsgi/api bootstrap
- `templates/` for shared templates; app-specific templates inside the app
- `static/` for global static assets; app-specific assets under `static/<app>/...`
- `tests/` with `tests/unittest/` and `tests/e2e/` when present
- `utils/` for reusable helpers

Avoid placing functional code in the repository root.

---

## 5. Naming conventions

### 5.1 Apps
- short, descriptive, lowercase, plural
- snake_case allowed for multi-word names (e.g., `song_reviews`)

### 5.2 Files (Python/HTML/JS/CSS)
- use **snake_case**
- keep one clear responsibility per file

### 5.3 Classes
- **PascalCase**
- generally **singular**
- Suffixes:
  - Forms end with `Form`
  - Class-based views end with `View`
  - Mixins end with `Mixin`
  - Services end with `Service`
  - Enums end with `Enum`

### 5.4 Variables and functions
- **snake_case**, descriptive names (avoid `data`, `item` unless contextual)

### 5.5 Constants
- **UPPER_SNAKE_CASE**

### 5.6 URLs
- Path/namespaces: **kebab-case**
- URL names: **snake_case**
Example:
- `disabled-index/` path, `name="disabled_index"`

---

## 6. Django Views: CBV only (FBV forbidden)

All Django views must be implemented as **Class-Based Views (CBVs)**.

You must:
- prefer internal generic views from the template when available:
  - `GenericCreateView`, `GenericUpdateView`, `GenericFilterView`, etc.
- otherwise use Django’s generic CBVs:
  - `CreateView`, `UpdateView`, `ListView`, etc.

You must **never** create Function-Based Views (FBVs).
If a requested change seems to require an FBV, propose a CBV alternative.

---

## 7. Validations: correct layer, no duplication

### 7.1 Model validations
- Use Django `validators=[...]` on fields where appropriate.
- Model validations protect integrity before persistence.

### 7.2 Schema validations (Django Ninja / Pydantic)
- Use Pydantic validators such as `@field_validator` for API input validation.
- Use separate schemas for **In** (request) and **Out** (response).

### 7.3 Form validations
Use:
- field validators (`validators=...`)
- `clean_<field>()` for single-field logic
- `clean()` for cross-field validation (`self.add_error(...)`)

### 7.4 View-level validations
Use view methods only for **business rules**, not for basic data integrity:
- `dispatch()` for access/permission/state checks
- `form_valid()` for business rules after form is valid
- `form_invalid()` for messaging/logging

**Do not** duplicate validations already enforced at the model/form/schema level.

---

## 8. Constants and user-facing messages

All backend user-facing strings (errors, labels, messages, etc.) must be:
1. centralized in constants (typically `consts.py`), and
2. marked as translatable using `gettext_lazy` (`_()`).

### 8.1 App-level constants
Each app should have `apps/<app_name>/consts.py` defining:
- `APP_NAME`, `MODEL_NAME`, `MODULE_VERBOSE_NAME`
- URL names, titles, list/detail fields, default ordering
- permission strings (`PERMISSION_VIEW`, `PERMISSION_ADD`, ...)

Views should import and use these constants instead of hardcoding strings.

### 8.2 Global constants
If a constant is shared across multiple apps, place it in:
- `<project_name>/consts.py`

No functions or logic in `consts.py` — constants only.

---

## 9. Django Ninja APIs: structure

When working on APIs, follow the modular structure:
- `apps/<app>/api/controller.py` (routing/controllers)
- `apps/<app>/api/schemas.py` (Pydantic/ModelSchema)
- `apps/<app>/api/service.py` (business logic)

Controllers must be thin; services encapsulate business rules.

### 9.1 Schemas
- Prefer `ModelSchema` for CRUD
- Use `Schema` for custom payloads
- Split request/response schemas (In vs Out)

### 9.2 Services
- Use/extend `GenericModelService` if available
- Keep HTTP concerns out of services (return data or raise exceptions, do not build HTTP responses)

---

## 10. .env conventions

- Never commit `.env` files.
- Keep `.env.example` complete and updated.
- Use uppercase with underscores; avoid ambiguous abbreviations.
- Group variables by category (DB, auth, URLs, etc.).

### 10.1 Internal vs external service URLs
Use:
- `<SERVICE>_URL_INTERNAL` for backend-to-backend comms inside the same environment
- `<SERVICE>_URL_EXTERNAL` for public/external access

In Docker, prefer `host-gateway` instead of `localhost` for host access.

---

## 11. Documentation rules (Python docstrings)

Python docstrings must follow **Google Python Style Guide**:
- triple double quotes `"""`
- written in **English**
- include sections as needed: Args, Returns, Raises, Example(s)

---

## 12. How the agent should perform a Code Review

When asked to review code (PR, diff, or patch), follow this checklist:

### 12.1 Scope and correctness
- Does the change match the ticket/task scope?
- Any unrelated modifications that should be removed?

### 12.2 Architecture consistency
- Django views are CBVs (no FBVs).
- API code follows controller/schema/service separation.
- Business logic stays in services/forms/models as appropriate.

### 12.3 Naming and structure
- Names follow conventions (PascalCase, snake_case, etc.).
- Files placed in correct folders (`apps/`, `api/`, etc.).

### 12.4 Validations
- Validation is implemented at the correct layer.
- No unnecessary duplication across model/schema/form/view.

### 12.5 Constants and translations
- No hardcoded user-visible strings.
- Strings are centralized in `consts.py` and wrapped with `_()`.

### 12.6 Testing & evidence
- Are there tests for the change (unit/integration/e2e as applicable)?
- If frontend changes exist: screenshots/GIF provided.
- If Playwright tests exist: Playwright HTML report provided.

### 12.7 Risk assessment
- Identify security concerns, performance issues, migration risk, backwards compatibility.
- Call out missing indexes, N+1 queries, missing pagination/filtering on list endpoints, etc.

### 12.8 Output format for reviews
When providing feedback:
- group comments by severity: **Blockers**, **Important**, **Nice-to-have**
- include actionable suggestions and (when possible) code snippets

---

## 13. If instructions conflict
If a request conflicts with these standards (e.g., “write an FBV”), you must:
1. explain the conflict briefly,
2. propose a compliant alternative (e.g., CBV),
3. ask for confirmation if the alternative changes the implementation approach.

---
