from uuid import UUID

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


def create_account(db: Session, account_data: AccountCreate) -> Account:
    account = Account(**account_data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account(db: Session, account_id: UUID) -> Account | None:
    return db.query(Account).filter(Account.id == account_id).first()


def get_account_by_google_id(db: Session, google_id: str) -> Account | None:
    """Look up an account by their Google ID — used during OAuth login."""
    return db.query(Account).filter(Account.google_id == google_id).first()


def get_account_by_email(db: Session, email: str) -> Account | None:
    """Look up an account by their email address."""
    return db.query(Account).filter(Account.email == email).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 20) -> list[Account]:
    return db.query(Account).offset(skip).limit(limit).all()


def update_account(db: Session, account_id: UUID, account_data: AccountUpdate) -> Account | None:
    account = get_account(db, account_id)
    if not account:
        return None

    for field, value in account_data.model_dump(exclude_unset=True).items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)
    return account


def deactivate_account(db: Session, account_id: UUID) -> bool:
    """Soft-delete: sets is_active to False instead of removing the row."""
    account = get_account(db, account_id)
    if not account:
        return False
    account.is_active = False
    db.commit()
    return True
