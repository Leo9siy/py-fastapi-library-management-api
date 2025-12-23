from fastapi import FastAPI

from books_routers import books_router
from author_routers import author_router

app = FastAPI()

app.include_router(author_router)
app.include_router(books_router)
