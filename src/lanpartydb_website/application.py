"""
lanpartydb_website.application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from collections import defaultdict
from pathlib import Path

from flask import Flask
from flask_babel import Babel
import jinja2

from .blueprints.base.views import blueprint as base_blueprint
from .blueprints.homepage.views import blueprint as homepage_blueprint
from .blueprints.party.views import blueprint as party_blueprint
from .blueprints.series.views import blueprint as series_blueprint
from .commands import register_commands
from . import loader


def create_app() -> Flask:
    app = Flask(__name__)

    # Throw an exception when an undefined name is referenced in a template.
    app.jinja_env.undefined = jinja2.StrictUndefined

    Babel(app)

    app.register_blueprint(base_blueprint)
    app.register_blueprint(homepage_blueprint)
    app.register_blueprint(party_blueprint)
    app.register_blueprint(series_blueprint)

    register_commands(app)

    _load_data(app)

    return app


def _load_data(app: Flask) -> None:
    data_path = Path('./data')

    app.data_commit_hash = loader.load_commit_hash(data_path)
    app.data_timestamp = loader.load_timestamp(data_path)

    series_list = loader.load_series(data_path)
    parties = loader.load_parties(data_path)

    series_by_slug = {series.slug: series for series in series_list}
    app.series_by_slug = series_by_slug

    party_counts_by_series_slug = defaultdict(int)
    for party in parties:
        if party.series_slug:
            party_counts_by_series_slug[party.series_slug] += 1

    app.series_and_party_counts = [
        (series, party_counts_by_series_slug[series.slug]) for series in series_list
    ]

    parties_by_slug = {party.slug: party for party in parties}
    app.parties_by_slug = parties_by_slug

    parties_by_series_slug = defaultdict(list)
    for party in parties:
        parties_by_series_slug[party.series_slug].append(party)
    for series_slug, parties in parties_by_series_slug.items():
        parties.sort(key=lambda party: party.start_on, reverse=True)

    app.parties_by_series_slug = parties_by_series_slug
