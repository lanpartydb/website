"""
lanpartydb_website.blueprints.homepage.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from flask import current_app

from ...util.blueprint import create_blueprint
from ...util.templating import templated


blueprint = create_blueprint('homepage', __name__, url_prefix='/')


@blueprint.get('/')
@templated
def index():
    return {
        'party_count': _count_parties(),
        'series_count': _count_series(),
        'country_count': _count_countries(),
    }


def _count_parties() -> int:
    parties = list(current_app.parties_by_slug.values())
    return len(parties)


def _count_series() -> int:
    series_list = current_app.series_by_slug.keys()
    return len(series_list)


def _count_countries() -> int:
    parties = list(current_app.parties_by_slug.values())
    country_codes = {party.location.country_code for party in parties if party.location}
    return len(country_codes)
