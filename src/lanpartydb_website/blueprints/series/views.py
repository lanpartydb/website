"""
lanpartydb_website.blueprints.series.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from flask import abort, current_app
from pycountry import countries
from pycountry.db import Country

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


@blueprint.get('/-/by-country/<country_code>/')
@templated
def index_by_country(country_code: str):
    country = _find_country(country_code)

    series_and_party_counts = [
        (series, party_count)
        for series, party_count in current_app.series_and_party_counts
        if country.alpha_2.lower() in series.country_codes
    ]

    return {
        'country': country,
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


def _find_country(country_code: str) -> Country | None:
    return countries.get(alpha_2=country_code)
