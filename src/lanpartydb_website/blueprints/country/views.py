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
    party_count: int


@blueprint.get('/')
@templated
def index():
    counter = Counter()
    for party in _get_parties():
        if party.location:
            counter[party.location.country_code] += 1

    country_codes_with_party_count = list(counter.items())

    countries_with_counts = []
    for country_code, party_count in country_codes_with_party_count:
        country = _find_country(country_code)

        countries_with_counts.append(
            CountryWithCounts(
                name=country.name,
                code=country.alpha_2.lower(),
                flag=country.flag,
                party_count=party_count,
            )
        )

    return {
        'countries_with_counts': countries_with_counts,
    }


def _get_parties() -> list[Party]:
    return list(current_app.parties_by_slug.values())


def _find_country(country_code: str) -> Country | None:
    return countries.get(alpha_2=country_code)
