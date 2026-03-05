"""
lanpartydb_website.blueprints.country.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from collections import Counter
from dataclasses import dataclass

from flask import abort, current_app, request
from flask_paginate import Pagination
from lanpartydb.models import Party
from pycountry import countries
from pycountry.db import Country

from ...util.blueprint import create_blueprint
from ...util.templating import templated


blueprint = create_blueprint('country', __name__, url_prefix='/countries')


@dataclass(frozen=True, slots=True)
class CountryWithCounts:
    name: str
    code: str
    flag: str
    series_count: int
    party_count: int


@blueprint.get('/')
@templated
def index():
    series_counts_by_country_code = _get_series_counts_by_country_code()
    party_counts_by_country_code = _get_party_counts_by_country_code()

    country_codes = set(party_counts_by_country_code.keys())

    countries_with_counts = []
    for country_code in country_codes:
        country = _find_country(country_code)

        countries_with_counts.append(
            CountryWithCounts(
                name=country.name,
                code=country.alpha_2.lower(),
                flag=country.flag,
                series_count=series_counts_by_country_code[country_code],
                party_count=party_counts_by_country_code[country_code],
            )
        )

    return {
        'countries_with_counts': countries_with_counts,
    }


def _get_series_counts_by_country_code() -> dict[str, int]:
    series_list = list(current_app.series_by_slug.values())

    counter = Counter(
        country_code
        for series in series_list
        for country_code in series.country_codes
    )

    return dict(counter.items())


def _get_party_counts_by_country_code() -> dict[str, int]:
    parties = list(current_app.parties_by_slug.values())

    counter = Counter(
        party.location.country_code for party in parties if party.location
    )

    return dict(counter.items())


def _find_country(country_code: str) -> Country | None:
    return countries.get(alpha_2=country_code)
