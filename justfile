_default:
    @just --list

deps-outdated:
    uv lock --dry-run --upgrade

freeze:
    uv run flask freeze

serve:
    uv run flask run --debug
