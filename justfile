_default:
    @just --list

# List dependency updates.
deps-outdated:
    uv lock --dry-run --upgrade

# Render website to static files.
freeze:
    uv run flask freeze

# Serve website through development server.
serve:
    uv run flask run --debug
