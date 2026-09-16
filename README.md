# Student Mini System

A professional but understandable Python CLI project for managing users, students, courses, enrollment, grades, averages, and top students. It uses only the Python standard library.

## Features
- Registration and login with PBKDF2 password hashing.
- Student and course management.
- Course enrollment.
- Grade entry/update with `0..100` validation.
- Student averages and top-student ranking.
- JSON persistence with UTF-8 and Arabic-safe output.
- Repository Pattern and Dependency Injection.
- Custom Exceptions, Decorators, Closures, Higher-Order Functions, `map`, `filter`, `sorted`, and `lambda`.
- `dataclass`, `Enum`, Type Hints, Docstrings, `*args`, `**kwargs`, positional-only `/`, and keyword-only `*`.
- Logging and `unittest`.

## Run
```bash
python -m app
```

## Tests
```bash
python -m unittest discover -s tests -v
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
Passwords are never saved as plain text. PBKDF2-HMAC-SHA256 with a random salt is used from the standard library.

## Concepts for presentation
- **Encapsulation:** `Student._grades` is private by convention and exposed through a validated property/setter and `set_grade`.
- **Dataclass:** `User`, `Student`, and `Course`.
- **Enum:** `UserRole` and `CourseLevel`.
- **Decorator:** `@requires_auth` and `@log_action`, both using `functools.wraps`.
- **Closure:** configurable course-name validator.
- **Higher-order functions:** transformation/filter functions receiving callables.
- **Sorting:** top students use `sorted(..., key=lambda ..., reverse=True)`.
- **Flexible arguments:** helper demonstrates `*args` and `**kwargs`.
- **Parameter kinds:** student grade uses positional-only `/`; student/course creation uses keyword-only `*`.
##Devloppers aws&mohmmed