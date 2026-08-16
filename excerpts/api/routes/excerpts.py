from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from excerpts.api.schemas import ExcerptCreate, ExcerptPublic, ExcerptsPublic, ExcerptUpdate
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source
from excerpts.types import DBDep, PaginationLimit, PaginationSkip

router = APIRouter(prefix="/excerpts", tags=["excerpts"])


@router.post("", response_model=ExcerptPublic, status_code=status.HTTP_201_CREATED)
def create_excerpt(excerpt_in: ExcerptCreate, db: DBDep) -> Excerpt:
    """
    Create new excerpt.
    """
    source_id = excerpt_in.source_id

    if not db.get(Source, source_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Could not find source with id {source_id}"
        )

    excerpt = Excerpt(
        content=excerpt_in.content,
        locator=excerpt_in.locator,
        meta=excerpt_in.meta,
        source_id=source_id,
    )
    db.add(excerpt)
    db.commit()
    db.refresh(excerpt)
    return excerpt


@router.get("", response_model=ExcerptsPublic)
def get_excerpts(db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 50) -> ExcerptsPublic:
    """
    Get excerpts.
    """
    total = db.scalar(select(func.count()).select_from(Excerpt)) or 0
    excerpts = db.scalars(
        select(Excerpt)
        .options(selectinload(Excerpt.source).selectinload(Source.author))
        .order_by(Excerpt.id)
        .offset(skip)
        .limit(limit)
    ).all()

    has_more = skip + len(excerpts) < total

    return ExcerptsPublic(
        data=[ExcerptPublic.model_validate(excerpt) for excerpt in excerpts],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{excerpt_id}", response_model=ExcerptPublic)
def get_excerpt(excerpt_id: int, db: DBDep) -> Excerpt:
    """
    Get excerpt by id.
    """
    excerpt = db.get(Excerpt, excerpt_id)

    if excerpt:
        return excerpt

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excerpt not found")


@router.patch("/{excerpt_id}", response_model=ExcerptPublic)
def update_excerpt(excerpt_id: int, excerpt_in: ExcerptUpdate, db: DBDep) -> Excerpt:
    """
    Update excerpt by id.
    """
    excerpt = db.get(Excerpt, excerpt_id)

    if not excerpt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excerpt not found")

    update_data = excerpt_in.model_dump(exclude_unset=True)

    if "source_id" in update_data and not db.get(Source, update_data["source_id"]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Could not find source with id {update_data['source_id']}",
        )

    for field, value in update_data.items():
        setattr(excerpt, field, value)

    db.commit()
    db.refresh(excerpt)
    return excerpt


@router.delete("/{excerpt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_excerpt(excerpt_id: int, db: DBDep) -> None:
    """
    Delete excerpt by id.
    """
    excerpt = db.get(Excerpt, excerpt_id)

    if not excerpt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excerpt not found")

    db.delete(excerpt)
    db.commit()
