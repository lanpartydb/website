"""
lanpartydb_website.blueprints.party.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from collections import Counter

from flask import abort, current_app, request
from flask_paginate import Pagination
from lanpartydb.models import Party
from pycountry import countries
from pycountry.db import Country

from ...util.blueprint import create_blueprint
from ...util.templating import templated


blueprint = create_blueprint('party', __name__, url_prefix='/parties')


@blueprint.get('/', defaults={'page': 1})
@blueprint.get('/-/pages/<int:page>/')
@templated
def index(page: int):
    per_page = request.args.get('per_page', type=int, default=50)
    offset = (page - 1) * per_page

    parties = _get_parties()
    parties.sort(key=lambda party: party.start_on, reverse=True)

    pagination = Pagination(page=page, per_page=per_page, total=len(parties))

    parties_slice = parties[offset : offset + per_page]

    return {
        'parties': parties_slice,
        'pagination': pagination,
        'countries': countries,
    }


@blueprint.get('/-/by-country/')
@templated
def index_countries():
    counter = Counter()
    for party in _get_parties():
        if party.location:
            counter[party.location.country_code] += 1

    country_codes_with_party_count = list(counter.items())

    countries_with_party_count = [
        (_find_country(country_code), party_count)
        for country_code, party_count in country_codes_with_party_count
    ]

    return {
        'countries_with_party_count': countries_with_party_count,
    }


@blueprint.get('/-/by-country/<country_code>/', defaults={'page': 1})
@blueprint.get('/-/by-country/<country_code>/pages/<int:page>/')
@templated
def index_by_country(country_code: str, page: int):
    country = _find_country(country_code)

    per_page = request.args.get('per_page', type=int, default=50)
    offset = (page - 1) * per_page

    parties = _get_parties()
    parties = filter(
        lambda party: _find_party_country_code(party) == country.alpha_2.lower(),
        parties,
    )
    parties = list(sorted(parties, key=lambda party: party.start_on, reverse=True))

    pagination = Pagination(page=page, per_page=per_page, total=len(parties))

    parties_slice = parties[offset : offset + per_page]

    return {
        'country': country,
        'parties': parties_slice,
        'pagination': pagination,
        'countries': countries,
    }


@blueprint.get('/<slug>/')
@templated
def view(slug: str):
    party = current_app.parties_by_slug.get(slug)
    if not party:
        abort(404)

    series = current_app.series_by_slug.get(party.series_slug)

    country = _find_party_country(party)

    return {
        'party': party,
        'series': series,
        'country': country,
    }


def _get_parties() -> list[Party]:
    return list(current_app.parties_by_slug.values())


def _find_party_country_code(party: Party) -> str | None:
    if not party.location:
        return None

    return party.location.country_code


def _find_party_country(party: Party) -> Country | None:
    country_code = _find_party_country_code(party)
    if not country_code:
        return None

    return _find_country(country_code)


def _find_country(country_code: str) -> Country | None:
    return countries.get(alpha_2=country_code)
