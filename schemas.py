from datetime import datetime

from pydantic import BaseModel, Field


class AuthorCreateSchema(BaseModel):
    name: str
    bio: str


class AuthorResponseSchema(AuthorCreateSchema):
    id: int

    model_config = True


class AuthorListSchema(BaseModel):
    authors: list[AuthorResponseSchema]

    model_config = True


class BookCreateSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime | None
    author_id: int


class BookResponseSchema(BookCreateSchema):
    id: int

    model_config = True


class BookListSchema(BaseModel):
    books: list[BookResponseSchema]

    model_config = True
