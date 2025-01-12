"""
lanpartydb_website.models
~~~~~~~~~~~~~~~~~~~~~~~~~

Data models

:Copyright: 2024-2025 Jochen Kupperschmidt
:License: MIT
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Contributor:
    github_login: str
    github_avatar_url: str
    contribution_count: int
