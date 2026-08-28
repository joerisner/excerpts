from fastapi import HTTPException, status
from sqlalchemy import select

from excerpts.models.tag import Tag
from excerpts.types import DBDep
from excerpts.utils.string import slugify


def get_or_404[T](db: DBDep, model: type[T], id: int) -> T:
    """
    Return a resource from the database or respond with a 404 response.
    """
    resource = db.get(model, id)

    if resource is not None:
        return resource

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")


def resolve_tags(db: DBDep, names: list[str]) -> list[Tag]:
    """
    Resolve tag names to Tag rows, creating any that don't already exist.

    Tags are keyed on their slug, so names that slugify to the same value
    (e.g. "Philosophy" and "philosophy") resolve to a single tag.
    """
    tags: list[Tag] = []
    seen: set[str] = set()

    for name in names:
        slug = slugify(name)

        if slug in seen:
            continue
        seen.add(slug)

        tag = db.scalar(select(Tag).where(Tag.slug == slug))
        if tag is None:
            tag = Tag(name=name, slug=slug)
            db.add(tag)

        tags.append(tag)

    return tags
