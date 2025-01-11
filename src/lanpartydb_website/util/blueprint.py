"""
lanpartydb_website.util.blueprint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Blueprint helpers

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from flask import Blueprint


def create_blueprint(
    name: str, import_name: str, *, url_prefix: str | None = None
) -> Blueprint:
    """Create a blueprint with default folder names."""
    return Blueprint(
        name,
        import_name,
        static_folder='static',
        template_folder='templates',
        url_prefix=url_prefix,
    )
