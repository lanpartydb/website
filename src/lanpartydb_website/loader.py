"""
lanpartydb_website.loader
~~~~~~~~~~~~~~~~~~~~~~~~~

Data loading

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from collections.abc import Iterator
from datetime import datetime
import json
from pathlib import Path

from lanpartydb.models import Party, Series
from lanpartydb.reading import (
    read_party_from_toml_file,
    read_series_list_from_toml_file,
)

from .models import Contributor


def load_commit_hash(data_path: Path) -> str:
    filename = data_path / 'commithash.txt'
    return filename.read_text().rstrip()


def load_timestamp(data_path: Path) -> datetime:
    filename = data_path / 'timestamp.txt'
    s = filename.read_text().rstrip()
    return datetime.fromisoformat(s)


def load_contributors(data_path: Path) -> list[Contributor]:
    filename = data_path / 'contributors.json'

    with filename.open() as f:
        data = json.load(f)

    def parse_data() -> Iterator[Contributor]:
        for item in data:
            yield Contributor(
                github_login=item['github_login'],
                github_avatar_url=item['github_avatar_url'],
                contribution_count=item['contribution_count'],
            )

    return list(parse_data())


def load_series(data_path: Path) -> list[Series]:
    filename = data_path / 'series.toml'
    return read_series_list_from_toml_file(filename)


def load_parties(data_path: Path) -> list[Party]:
    parties_path = data_path / 'parties'
    party_filenames = parties_path.glob('**/*.toml')
    return list(map(read_party_from_toml_file, party_filenames))
