from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Engine = the connection pool to the database (like a DataSource in Spring)
engine = create_engine(settings.database_url)

# SessionLocal = a factory that produces new database sessions (like @Transactional scoped sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that provides a database session per request.
    This is the equivalent of Spring's @Autowired EntityManager —
    FastAPI injects it into route handlers via Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
