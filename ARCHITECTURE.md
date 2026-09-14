# Architecture

## Layers

### CLI
Collects input and prints output. It does not read or write JSON directly.

### Services
Contains business logic such as registration, enrollment, grade validation, averages, and ranking. Repositories are injected into services through constructors.

### Repositories
Own JSON persistence. The `json` module is isolated to this layer.

### Models
Represent domain objects using dataclasses, properties, validation, and useful magic methods.

## Dependency direction
```text
CLI -> Services -> Repositories -> JSON

                 -> Models
```

## Concepts
- Repository Pattern separates storage from business logic.
- Dependency Injection makes services testable with fake repositories.
- Decorators provide authentication and logging without duplicating code.
- Custom Exceptions communicate expected failures.
- `pathlib` centralizes safe file paths.
- Standard-library `unittest` tests models and services without touching production JSON files.
