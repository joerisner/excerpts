from fastapi import HTTPException, status

from excerpts.types import DBDep


def get_or_404[T](db: DBDep, model: type[T], id: int) -> T:
    """
    Return a resource from the database or respond with a 404 response.
    """
    resource = db.get(model, id)

    if resource is not None:
        return resource

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
