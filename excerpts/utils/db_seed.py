"""
Seed the local development database.
This script should only ever run in the `dev` environment.
"""

from excerpts.core.config import config
from excerpts.core.db import SessionLocal
from excerpts.models.author import Author
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source

AUTHORS = [
    {"first_name": "Ross", "last_name": "Geller"},
    {"first_name": "Rachel", "last_name": "Green"},
    {"first_name": "Monica", "last_name": "Geller"},
    {"first_name": "Chandler", "last_name": "Bing"},
    {"first_name": "Joey", "last_name": "Tribbiani"},
    {"last_name": "Gunther"},
]

SOURCES = [
    {"title": "Dinosaurs and Other Things I Was Right About", "type": "book", "author_id": 1},
    {"title": "From Waitress to Runway", "type": "book", "author_id": 2},
    {"title": "A Place for Everything: The Geller Method", "type": "book", "author_id": 3},
    {"title": "Could I BE Any More Sarcastic?", "type": "book", "author_id": 4},
    {"title": "Joey Doesn't Share Food", "type": "book", "author_id": 5},
    {"title": "We Were on a Break", "type": "essay", "author_id": 1},
    {"title": "How to Make a Traditional English Trifle", "type": "article", "author_id": 2},
    {"title": "Seven Steps to a Spotless Apartment", "type": "video", "author_id": 3},
    {"title": "The Transponster", "type": "podcast", "author_id": 4},
    {"title": "Dr. Drake Ramoray: Best of Days of Our Lives", "type": "video", "author_id": 5},
    {"title": "The Man Behind the Counter", "type": "book", "author_id": 6},
]

EXCERPTS = [
    {
        "content": "Pivot! Pivot! PIVOT!",
        "locator": "Page 88",
        "source_id": 1,
        "meta": {"season": 5, "episode": "The One with the Cop", "tags": ["couch", "moving"]},
    },
    {
        "content": "Unagi. It's a state of total awareness.",
        "locator": "Page 140",
        "source_id": 1,
    },
    {
        "content": "We were on a break!",
        "locator": "Paragraph 1",
        "source_id": 6,
    },
    {
        "content": "It's like all my life everyone has told me, 'You're a shoe!' Well, what if I don't want to be a shoe?",  # noqa: E501
        "locator": "Page 3",
        "source_id": 2,
        "meta": {"season": 1, "episode": "Pilot", "tags": ["independence"]},
    },
    {
        "content": "I got off the plane.",
        "locator": "Page 291",
        "source_id": 2,
    },
    {
        "content": "First a layer of ladyfingers, then a layer of jam, then custard, which I made from scratch.",
        "locator": "Step 1",
        "source_id": 7,
    },
    {
        "content": "Rules are good! Rules help control the fun!",
        "locator": "Page 12",
        "source_id": 3,
    },
    {
        "content": "Welcome to the real world. It sucks. You're gonna love it.",
        "locator": "Page 1",
        "source_id": 3,
    },
    {
        "content": "I KNOW!",
        "locator": "00:03:15",
        "source_id": 8,
    },
    {
        "content": "Hi, I'm Chandler. I make jokes when I'm uncomfortable.",
        "locator": "Page 7",
        "source_id": 4,
    },
    {
        "content": "Could I BE any more sarcastic?",
        "locator": "Page 42",
        "source_id": 4,
    },
    {
        "content": "My job is statistical analysis and data reconfiguration.",
        "locator": "00:11:30",
        "source_id": 9,
    },
    {
        "content": "How you doin'?",
        "locator": "Page 1",
        "source_id": 5,
        "meta": {"season": 4, "tags": ["catchphrase", "flirting"]},
    },
    {
        "content": "Joey doesn't share food!",
        "locator": "Page 55",
        "source_id": 5,
    },
    {
        "content": "I'm Dr. Drake Ramoray, neurosurgeon.",
        "locator": "00:02:47",
        "source_id": 10,
    },
    {
        "content": "Rachel... I love you.",
        "locator": "Page 212",
        "source_id": 11,
        "meta": {"season": 10, "episode": "The Last One", "tags": ["confession", "central-perk"]},
    },
]


def seed_authors() -> None:
    with SessionLocal() as session:
        session.add_all([Author(**author) for author in AUTHORS])
        session.commit()


def seed_sources() -> None:
    with SessionLocal() as session:
        session.add_all([Source(**source) for source in SOURCES])
        session.commit()


def seed_excerpts() -> None:
    with SessionLocal() as session:
        session.add_all([Excerpt(**excerpt) for excerpt in EXCERPTS])
        session.commit()


def main() -> None:
    seed_authors()
    seed_sources()
    seed_excerpts()


if __name__ == "__main__":
    if config.ENVIRONMENT != "dev":
        raise RuntimeError("Seed script should only run in dev environment")
    main()
