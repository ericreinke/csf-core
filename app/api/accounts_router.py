from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.services import account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    # Check for duplicate google_id
    if account_service.get_account_by_google_id(db, account_data.google_id):
        raise HTTPException(status_code=409, detail="Account with this Google ID already exists")
        
    # Check for duplicate email
    if account_service.get_account_by_email(db, account_data.email):
        raise HTTPException(status_code=409, detail="Account with this email already exists")
        
    return account_service.create_account(db, account_data)


@router.get("/", response_model=list[AccountResponse])
def get_accounts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return account_service.get_accounts(db, skip=skip, limit=limit)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: UUID, db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(account_id: UUID, account_data: AccountUpdate, db: Session = Depends(get_db)):
    account = account_service.update_account(db, account_id, account_data)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete("/{account_id}", status_code=204)
def deactivate_account(account_id: UUID, db: Session = Depends(get_db)):
    if not account_service.deactivate_account(db, account_id):
        raise HTTPException(status_code=404, detail="Account not found")
