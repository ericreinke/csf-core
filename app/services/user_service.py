from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_google_id(db: Session, google_id: str) -> User | None:
    """Look up a user by their Google ID — used during OAuth login."""
    return db.query(User).filter(User.google_id == google_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Look up a user by their email address."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 20) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: UUID) -> bool:
    """Soft-delete: sets is_active to False instead of removing the row."""
    user = get_user(db, user_id)
    if not user:
        return False
    user.is_active = False
    db.commit()
    return True
