# Local development

## Setup
We highly recommend to use provided script to setup everything by single command.
Just run the following command from project's root directory and follow instructions:
* `bin/setup`

That's all!


## Style guides and name conventions

### Linters and code-formatters
We use git-hooks to run linters and formatters before any commit.
It installs git-hooks automatically if you used `bin/setup` command.
So, if your commit is failed then check console to see details and fix linter issues.

We use:

* mypy - static type checker
* ruff-format - code formatter
* ruff - logical and stylistic lint, security linter, and more
* safety - security check for requirements

## Git Standards

### Commit Message Format
Use semantic commits for clear change tracking:

```
feat(user): Add ability to reset password
fix(login): Fix issue preventing users from logging in
refactor(payment): Simplify payment processing code
style(user): Format user profile page
```

### Commit Types:
- **feat**: A new feature or enhancement to existing functionality
- **fix**: A bug fix or correction to existing functionality  
- **refactor**: Changes that improve code structure, readability, or maintainability without adding features or fixing bugs
- **style**: Changes to formatting, code layout that do not affect functionality

### Workflow:
- Work directly on main branch for most changes
- Use feature branches only for experimental or large changes
- Commit frequently with descriptive messages
- Each commit should represent a logical unit of work
