from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from excerpts.api.schemas.author import AuthorCreate, AuthorPublic, AuthorsPublic, AuthorUpdate
from excerpts.api.schemas.source import SourcePublic, SourcesPublic
from excerpts.models.author import Author
from excerpts.models.source import Source
from excerpts.types import DBDep, PaginationLimit, PaginationSkip

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("", response_model=AuthorPublic, status_code=status.HTTP_201_CREATED)
def create_author(author_in: AuthorCreate, db: DBDep) -> Author:
    """
    Create new author.
    """
    stmt = select(Author).where(func.lower(Author.last_name) == author_in.last_name.lower())

    if author_in.first_name is not None:
        stmt = stmt.where(func.lower(Author.first_name) == author_in.first_name.lower())
    else:
        stmt = stmt.where(Author.first_name.is_(None))

    existing_author = db.scalars(stmt).first()

    if existing_author:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author already exists with that name")

    author = Author(first_name=author_in.first_name, last_name=author_in.last_name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.get("", response_model=AuthorsPublic)
def get_authors(db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 20) -> AuthorsPublic:
    """
    Get authors.
    """
    total = db.scalar(select(func.count()).select_from(Author)) or 0
    authors = db.scalars(select(Author).order_by(Author.id).offset(skip).limit(limit)).all()

    has_more = skip + len(authors) < total

    return AuthorsPublic(
        data=[AuthorPublic.model_validate(author) for author in authors],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{author_id}", response_model=AuthorPublic)
def get_author(author_id: int, db: DBDep) -> Author:
    """
    Get author by id.
    """
    author = db.get(Author, author_id)

    if author:
        return author

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")


@router.patch("/{author_id}", response_model=AuthorPublic)
def update_author(author_id: int, author_in: AuthorUpdate, db: DBDep) -> Author:
    """
    Update author by id.
    """
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    update_data = author_in.model_dump(exclude_unset=True)  # Do not set default values for fields not explicitly set.

    # As in create_author, we reject updates that would duplicate an existing author.
    first_name = update_data.get("first_name", author.first_name)
    last_name = update_data.get("last_name", author.last_name)
    stmt = select(Author).where(Author.id != author_id).where(func.lower(Author.last_name) == last_name.lower())

    if first_name is not None:
        stmt = stmt.where(func.lower(Author.first_name) == first_name.lower())
    else:
        stmt = stmt.where(Author.first_name.is_(None))

    if db.scalars(stmt).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author already exists with that name")

    for field, value in update_data.items():
        setattr(author, field, value)

    db.commit()
    db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: DBDep) -> None:
    """
    Delete author by id.
    """
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    db.delete(author)
    db.commit()


@router.get("/{author_id}/sources", response_model=SourcesPublic)
def get_author_sources(
    author_id: int, db: DBDep, skip: PaginationSkip = 0, limit: PaginationLimit = 20
) -> SourcesPublic:
    """
    Get sources that belong to an author.
    """
    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    total = db.scalar(select(func.count()).select_from(Source).where(Source.author_id == author_id)) or 0
    sources = db.scalars(
        select(Source).where(Source.author_id == author_id).order_by(Source.id).offset(skip).limit(limit)
    ).all()

    has_more = skip + len(sources) < total

    return SourcesPublic(
        data=[SourcePublic.model_validate(source) for source in sources],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )
