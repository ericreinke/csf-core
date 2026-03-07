from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Every model (League, Player, etc.) will inherit from this.

    In Spring terms, this is like a @MappedSuperclass —
    it doesn't create its own table, but all subclasses get
    registered with SQLAlchemy's metadata system for migrations
    and table creation.
    """
    pass
