from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    url="sqlite:///sqlite3",
    echo=True
)

make_session = sessionmaker(
    bind=engine,
    autoflush=False,
)

def get_session():
    with make_session() as session:
        yield session
