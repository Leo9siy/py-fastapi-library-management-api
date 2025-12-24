from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import AuthorModel, BookModel
from schemas import AuthorCreateSchema, AuthorResponseSchema, BookCreateSchema


def add_book(db: Session, book_data: BookCreateSchema):
    book = BookModel(
        title=book_data.title,
        summary=book_data.summary,
        author_id=book_data.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def select_author_books(db: Session, limit: int = 10, skip: int = 0, author_id: int = None):
    books = db.query(BookModel).offset(skip).limit(limit)
    if author_id:
        books = books.filter(BookModel.author_id == author_id)

    return books.all()


def add_author(db: Session, author_data: AuthorCreateSchema):
    if db.query(AuthorModel).where(AuthorModel.name == author_data.name).count() != 0:
        raise HTTPException(
            status_code=409,
            detail=f"Author with {author_data.name} already exists"
        )

    author = AuthorModel(
        name=author_data.name,
        bio=author_data.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def select_author_by_id(
        author_id: int,
        db: Session
):
    author = db.query(AuthorModel).where(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


def select_authors(db: Session, skip: int = 0, limit: int = 10):
    authors = db.query(AuthorModel).offset(skip).limit(limit).all()
    return authors
