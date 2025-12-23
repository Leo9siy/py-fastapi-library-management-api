from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy.orm import Session

from database import get_session
from models import BookModel
from schemas import BookCreateSchema, BookResponseSchema, BookListSchema

books_router = APIRouter()


@books_router.post(
    path="/books/",
    response_model=BookResponseSchema,
    description="Create a new book for a specific author.",
    status_code=201,
)
def create_book(
        book_data: BookCreateSchema,
        db: Session = Depends(get_session),

):
    book = BookModel(
        title=book_data.title,
        summary=book_data.summary,
        author_id=book_data.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return BookResponseSchema.model_validate(book)


@books_router.get(
    path="/books/",
    response_model=BookListSchema,
    description="Retrieve a list of books with pagination (skip, limit).",
    summary="Filter books by author ID.",
    status_code=200
)
def get_books(
        author: int | None = Query(),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        db: Session = Depends(get_session),
):
    books = db.query(BookModel).offset(skip).limit(limit)
    if author:
        books.filter(BookModel.author_id == author)

    return BookListSchema.model_validate(books.all())
