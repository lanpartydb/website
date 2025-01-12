"""
lanpartydb_website.blueprints.base.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from datetime import datetime, UTC
from typing import Any

from flask import current_app

from ...util.blueprint import create_blueprint


blueprint = create_blueprint('base', __name__)


@blueprint.app_context_processor
def extend_template_context() -> dict[str, Any]:
    return {
        'data_commit_hash': current_app.data_commit_hash,
        'data_timestamp': current_app.data_timestamp,
        'data_contributors': current_app.data_contributors,
        'now': datetime.now(UTC),
    }
