# Django Internationalization & Style Refactor Prompt

Refactor this file to comply with our internationalization, architecture, and style standards.

---

## 1. Language and Internationalization Rules

### 1.1 User-Facing Strings

- Detect all user-facing text.
- Ensure every user-facing string is properly internationalized.
- Do NOT use f-strings, string concatenation, or `.format()` inside translation functions.
- Always use named placeholders for dynamic values.

### Python files

Wrap strings using:

```python
from django.utils.translation import gettext_lazy as _
```

if `_` is not imported, add t.
Use named placeholders:

```python
_("El estado {status} no es válido.").format(status=status)
```

NOT

```py
_(f"Estado {status} inválido")
```

NOT:

```py
 _("Estado {} inválido".format(status))
```

### Django templates

- Use {% trans %} for static text.
- Use {% blocktrans %} for dynamic values.
- Do not concatenate strings inside templates.
- Do not hardcode user-facing text.

### 1.2 Language Rules

- All user-facing text must be in Spanish.
- All comments must be written in English.
- All docstrings must be written in English.
- If any user-facing text is in English, translate it to Spanish.
- Use sentence case only (never title case).

## 2. Python File Rules

### 2.1 Constants Extraction

- Move all user-facing strings to consts.py inside the same app.
- Define them using gettext_lazy as `_`.
- Use clear, descriptive constant names in English.
- The actual message content must be in Spanish.
- Constants must NOT use f-strings.
- Constants must use named placeholders if dynamic.
Example:

```python
ERROR_INVALID_STATUS = _("Estado inválido.")
ERROR_INVALID_USER = _("El usuario {username} no es válido.")
```

### 2.2 Lazy Translation Safety

- Do not evaluate translations at import time.
- If a string includes dynamic content, define only the base string as a constant and format it at runtime.
- The above does not apply always, there are some cases inside the same `consts.py` where module name is in the same consts and won't change later

### 2.3 Comments and Docstrings

- Convert all comments to English.
- Ensure all docstrings:
  - Are written in English.
  - Follow Google style.
  - Clearly describe:
    - Purpose
    - Arguments
    - Return values
    - Side effects
    - Business meaning when applicable.

## 3. Special Rules for models.py

If this file is a models.py file:

### 3.1 Meta Configuration

- Add verbose_name and verbose_name_plural in Spanish.
- Wrap them with `_()`.
- Use sentence case and capitalize.

### 3.2 Field Labels

- Add `verbose_name` to all fields.
- In Spanish.
- Wrapped with `_()`.

### 3.3 Model Docstring

Each model must include a Google-style docstring in English explaining:

- Business meaning
- Domain context
- Important constraints
- Side effects
- Relationships

## 4. Structural Requirements

- Do not modify existing business logic.
- Do not change runtime behavior.
- Do not alter method signatures.
- Do not rename database fields.
- Only refactor for:
  - Internationalization
  - Structural consistency
  - Documentation quality
  - Django best practices compliance

## 5. Output Requirements

- Return the fully refactored file.
- Ensure the file is production-ready.
- Ensure:
  - No f-strings inside translation calls.
  - No concatenated translation strings.
  - No hardcoded user-facing text.
  - Proper lazy translation usage.
  - No duplicate translation entries.
  - Sentence case consistency.
