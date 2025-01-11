"""
lanpartydb_website.blueprints.series.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from flask import abort, current_app
from pycountry import countries

from ...util.blueprint import create_blueprint
from ...util.templating import templated


blueprint = create_blueprint('series', __name__, url_prefix='/series')


@blueprint.get('/')
@templated
def index():
    series_and_party_counts = current_app.series_and_party_counts

    return {
        'series_and_party_counts': series_and_party_counts,
        'countries': countries,
    }


@blueprint.get('/<slug>/')
@templated
def view(slug: str):
    series = current_app.series_by_slug.get(slug)
    if not series:
        abort(404)

    parties = current_app.parties_by_series_slug.get(series.slug)

    return {
        'series': series,
        'parties': parties,
        'countries': countries,
    }
