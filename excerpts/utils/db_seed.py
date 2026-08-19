"""
Seed the local development database.
This script should only ever run in the `dev` environment.
"""

from excerpts.core.config import config
from excerpts.core.db import SessionLocal
from excerpts.models.author import Author
from excerpts.models.excerpt import Excerpt
from excerpts.models.excerpt_tag import ExcerptTag
from excerpts.models.source import Source
from excerpts.models.tag import Tag

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
        "meta": {"season": 5, "episode": "The One with the Cop"},
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
        "meta": {"season": 1, "episode": "Pilot"},
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
        "meta": {"season": 4},
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
        "meta": {"season": 10, "episode": "The Last One"},
    },
]

TAGS = [
    {"name": "Independence", "slug": "independence"},
    {"name": "confession", "slug": "confession"},
    {"name": "Central Perk", "slug": "central-perk"},
    {"name": "catchphrase", "slug": "catchphrase"},
    {"name": "confidence", "slug": "confidence"},
    {"name": "Sarcasm", "slug": "sarcasm"},
]

EXCERPT_TAGS = [
    {"excerpt_id": 2, "tag_id": 5},
    {"excerpt_id": 9, "tag_id": 5},
    {"excerpt_id": 13, "tag_id": 4},
    {"excerpt_id": 13, "tag_id": 5},
    {"excerpt_id": 16, "tag_id": 2},
    {"excerpt_id": 14, "tag_id": 3},
    {"excerpt_id": 4, "tag_id": 1},
    {"excerpt_id": 8, "tag_id": 1},
    {"excerpt_id": 8, "tag_id": 6},
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


def seed_tags() -> None:
    with SessionLocal() as session:
        session.add_all([Tag(**tag) for tag in TAGS])
        session.commit()


def seed_excerpt_tags() -> None:
    with SessionLocal() as session:
        session.add_all([ExcerptTag(**excerpt_tag) for excerpt_tag in EXCERPT_TAGS])
        session.commit()


def main() -> None:
    seed_authors()
    seed_sources()
    seed_excerpts()
    seed_tags()
    seed_excerpt_tags()


if __name__ == "__main__":
    if config.ENVIRONMENT != "dev":
        raise RuntimeError("Seed script should only run in dev environment")
    main()
