from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from excerpts.api.schemas.tag import TagCreate, TagPublic, TagsPublic, TagUpdate
from excerpts.api.utils import get_or_404
from excerpts.models.tag import Tag
from excerpts.types import DBDep, PaginationLimit, PaginationSkip

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=TagPublic, status_code=status.HTTP_201_CREATED)
def create_tag(tag_in: TagCreate, db: DBDep) -> Tag:
    """
    Create new tag.
    """
    existing_tag = db.scalars(select(Tag).where(Tag.slug == tag_in.slug)).first()

    if existing_tag:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")

    tag = Tag(name=tag_in.name, slug=tag_in.slug)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("", response_model=TagsPublic)
def get_tags(db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 50) -> TagsPublic:
    """
    Get tags.
    """
    total = db.scalar(select(func.count()).select_from(Tag)) or 0
    tags = db.scalars(select(Tag).order_by(Tag.id).offset(skip).limit(limit)).all()

    has_more = skip + len(tags) < total

    return TagsPublic(
        data=[TagPublic.model_validate(tag) for tag in tags],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{tag_id}", response_model=TagPublic)
def get_tag(tag_id: int, db: DBDep) -> Tag:
    """
    Get tag by id.
    """
    return get_or_404(db=db, model=Tag, id=tag_id)


@router.patch("/{tag_id}", response_model=TagPublic)
def update_tag(tag_id: int, tag_in: TagUpdate, db: DBDep) -> Tag:
    """
    Update tag by id.
    """
    tag = get_or_404(db=db, model=Tag, id=tag_id)
    existing_tag = db.scalars(select(Tag).where(Tag.id != tag_id).where(Tag.slug == tag_in.slug)).first()

    if existing_tag:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")

    update_data = tag_in.model_dump()
    for field, value in update_data.items():
        setattr(tag, field, value)

    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: DBDep) -> None:
    """
    Delete tag by id.
    """
    tag = get_or_404(db=db, model=Tag, id=tag_id)

    db.delete(tag)
    db.commit()
