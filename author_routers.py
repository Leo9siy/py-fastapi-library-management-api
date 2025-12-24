from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from crud import add_author, select_authors
from database import get_session
from models import AuthorModel
from schemas import AuthorResponseSchema, AuthorCreateSchema, AuthorListSchema


author_router = APIRouter()


@author_router.post(
    path="/authors/",
    response_model=AuthorResponseSchema,
    description="Create a new author.",
    status_code=201
)
def create_author(
        author_data: AuthorCreateSchema,
        db: Session = Depends(get_session)
):
    return AuthorResponseSchema.model_validate(
        add_author(db, author_data)
    )


@author_router.get(
    path="/authors/",
    response_model=AuthorListSchema,
    status_code=200,
    description="Retrieve a list of authors with pagination (skip, limit)."
)
def get_authors(
        db: Session = Depends(get_session),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1)
):
    return AuthorListSchema(authors=select_authors(db, skip, limit))


@author_router.get(
    path="/authors/{author_id}/",
    response_model=AuthorResponseSchema,
    status_code=200,
    description="Retrieve a single author by ID."
)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_session),
):
    author = db.query(AuthorModel).where(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return AuthorResponseSchema.model_validate(author)
