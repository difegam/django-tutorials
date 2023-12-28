# Available recipes
_default:
    @just --list --unsorted --list-prefix "    > " --justfile {{justfile()}}

# Run pre-commit hooks
pre-commit:
    @pre-commit run --all-files