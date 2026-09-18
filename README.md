## عمل الطالب / محمد خالد مرشد قايد العلوي   &   الطالب /اوسان مثنى
# Student Mini System

A structured Python CLI project for managing users, students, courses, enrollment, grades, averages, and top students. The application runtime uses only the Python standard library; development tests use `pytest`.

## Features
- Registration and login with PBKDF2-HMAC-SHA256 password hashing.
- Student and course management.
- Course enrollment and grade entry/update with `0..100` validation.
- Student averages and top-student ranking.
- JSON persistence with UTF-8 and Arabic-safe output.
- Repository Pattern and Dependency Injection.
- Custom Exceptions, Decorators, Closures, Higher-Order Functions, `map`, `filter`, `sorted`, and `lambda`.
- `dataclass`, `Enum`, Type Hints, Docstrings, `*args`, `**kwargs`, positional-only `/`, and keyword-only `*`.

## Run
```bash
python -m app
```

## Tests
```bash
python -m pytest -q
```

## Architecture
```text
CLI
 ↓
Services
 ↓
Repositories
 ↓
JSON files
```

Models contain domain data and validation. Services contain business rules. Repositories isolate JSON persistence. The CLI handles user interaction only.

## Authentication
Passwords are never saved as plain text. PBKDF2-HMAC-SHA256 with a random salt is used from the Python standard library.

## Concepts for presentation
- **Encapsulation:** `Student._grades` is private by convention and exposed through validated methods/properties.
- **Dataclass:** `User`, `Student`, and `Course`.
- **Enum:** `UserRole` and `CourseLevel`.
- **Decorator:** `@requires_auth` and `@log_action`, both using `functools.wraps`.
- **Closure:** configurable course-name validator.
- **Higher-order functions:** reusable transformation/filter helpers receiving callables.
- **Sorting:** top students use `sorted(..., key=lambda ..., reverse=True)`.
- **Flexible arguments:** `format_record` demonstrates `*args` and `**kwargs`.
- **Parameter kinds:** student grade uses positional-only `/`; student/course creation uses keyword-only `*`.

## Course evidence
Final screenshots and terminal verification are stored under `docs/`.

## Developers
aws & mohmmmed
