"""
lanpartydb_website.commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom Flask commands

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

import logging
import sys

from flask import current_app, Flask
from flask_frozen import Freezer


def register_commands(app: Flask) -> None:
    app.cli.command()(freeze)


def freeze():
    """Export the application to static files."""
    # Log to STDERR to trace otherwise hidden errors.
    current_app.logger.addHandler(logging.StreamHandler(sys.stderr))

    current_app.config['FREEZER_BASE_URL'] = 'https://lanpartydb.orgatalk.de/'
    current_app.config['FREEZER_DESTINATION'] = '../../build'

    freezer = Freezer(current_app)

    # TODO
    # @freezer.register_generator
    # def url_generator() ->

    print('Freezing ...', end=' ')
    freezer.freeze()
    print('done.')
