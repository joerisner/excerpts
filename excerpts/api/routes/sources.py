from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from excerpts.api.schemas.excerpt import ExcerptPublic, ExcerptsPublic
from excerpts.api.schemas.source import SourceCreate, SourcePublic, SourcesPublic, SourceUpdate
from excerpts.api.utils import get_or_404
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source
from excerpts.types import DBDep, PaginationLimit, PaginationSkip

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourcePublic, status_code=status.HTTP_201_CREATED)
def create_source(source_in: SourceCreate, db: DBDep) -> Source:
    """
    Create new source.
    """
    existing_source = db.scalars(
        select(Source)
        .where(Source.author_id == source_in.author_id)
        .where(func.lower(Source.title) == source_in.title.lower())
    ).first()

    if existing_source:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Source by that title and author already exists"
        )

    source = Source(
        title=source_in.title,
        cover_image_file=source_in.cover_image_file,
        type=source_in.type,
        author_id=source_in.author_id,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("", response_model=SourcesPublic)
def get_sources(db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 20) -> SourcesPublic:
    """
    Get sources.
    """
    total = db.scalar(select(func.count()).select_from(Source)) or 0
    sources = db.scalars(
        select(Source).options(selectinload(Source.author)).order_by(Source.id).offset(skip).limit(limit)
    ).all()

    has_more = skip + len(sources) < total

    return SourcesPublic(
        data=[SourcePublic.model_validate(source) for source in sources],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{source_id}", response_model=SourcePublic)
def get_source(source_id: int, db: DBDep) -> Source:
    """
    Get source by id.
    """
    return get_or_404(db=db, model=Source, id=source_id)


@router.patch("/{source_id}", response_model=SourcePublic)
def update_source(source_id: int, source_in: SourceUpdate, db: DBDep) -> Source:
    """
    Update source by id.
    """
    source = get_or_404(db=db, model=Source, id=source_id)
    update_data = source_in.model_dump(exclude_unset=True)

    # As in create_source, we reject updates that would duplicate an existing source.
    title = update_data.get("title", source.title)
    author_id = update_data.get("author_id", source.author_id)
    existing_source = db.scalars(
        select(Source)
        .where(Source.id != source_id)
        .where(Source.author_id == author_id)
        .where(func.lower(Source.title) == title.lower())
    ).first()

    if existing_source:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Source by that title and author already exists"
        )

    for field, value in update_data.items():
        setattr(source, field, value)

    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(source_id: int, db: DBDep) -> None:
    """
    Delete source by id.
    """
    source = get_or_404(db=db, model=Source, id=source_id)

    db.delete(source)
    db.commit()


@router.get("/{source_id}/excerpts", response_model=ExcerptsPublic)
def get_source_excerpts(
    source_id: int, db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 50
) -> ExcerptsPublic:
    """
    Get excerpts that belong to a source.
    """
    get_or_404(db=db, model=Source, id=source_id)

    total = db.scalar(select(func.count()).select_from(Excerpt).where(Excerpt.source_id == source_id)) or 0
    excerpts = db.scalars(
        select(Excerpt)
        .options(selectinload(Excerpt.tags))
        .where(Excerpt.source_id == source_id)
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
