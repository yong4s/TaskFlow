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

### Branch and commit naming convention

We follow gitflow's branch model:

* `feature/NAME` - for any tasks, improvements
* `bugfix/NAME` - for bugs that will be released to staging/dev only
* `hotfix/NAME` - for hotfixes that will be released to the live

NAME should follow these rules:

* NAME should start with task ID, eg. `feature/MYPROJ-2020`
* add a short description to name with lowercase and using hyphen between words: e.g `feature/MYPROJ-2020-add-new-button-to-create-user`

All commit's comments should start with task ID and then a short description. For example:

* `MYPROJ-2895 - fixed bug related to some feature`
* `MYPROJ-2859 - Implemented new functionality`


### Pull request merge flow

Each developer should merge his own pull requests. Highly recommended the following settings:

* The main branches (`develop`, `master`, `staging`, etc.) should be protected for merging into these branches directly, **only through pull requests**.
* At least one approve required in order to have ability to merge the pull request.
