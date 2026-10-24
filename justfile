_default:
    @just --list

deps-outdated:
    uv tree --all-groups --depth 1 --no-dev --outdated

serve:
    uv run flask run --debug
