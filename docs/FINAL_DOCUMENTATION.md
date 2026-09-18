# Final Project Documentation

## Project
Student Mini System is a Python command-line application organized into CLI, service, repository, model, and core layers.

## Course requirements demonstrated

### Linux commands
Git Bash was used to demonstrate shell navigation, file listing, search, disk usage, and filesystem information.

Evidence:
- `docs/screenshots/01-linux-commands.png`
- `docs/screenshots/01-linux-commands2.png`

### Git and GitHub
The repository contains real commit history, a merged pull request, branch history, and a public GitHub repository.

Evidence:
- `docs/screenshots/02-git-status.png`
- `docs/screenshots/03-git-history.png`
- `docs/screenshots/04-github-repository.png`

### Clean Coding
The project separates responsibilities across models, services, repositories, CLI, configuration, exceptions, decorators, and utilities. Functions and classes use descriptive names, type hints, docstrings, validation, and custom exceptions.

Evidence:
- `docs/screenshots/05-clean-code.png`

### Testing and final verification
Automated tests verify password hashing, configuration file creation, application imports, grade validation, and student averages.

Evidence:
- `docs/screenshots/06-tests.png`
- `docs/screenshots/07-program-run.png`

### Vibe Coding / AI-assisted development
AI assistance was used to review code, identify missing modules, troubleshoot imports, improve structure, and verify the final application. Suggestions were reviewed, executed, tested, and committed through Git.

Evidence:
- `docs/screenshots/08-vibe-coding.png`

## Final verification commands
```bash
python -m pytest -q
python -m app
git status
git log --oneline --graph --decorate --all -n 20
```

> The screenshots were captured during final verification. Git and GitHub history preserve the actual repository development record.
