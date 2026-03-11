from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate google_id or email
    existing = user_service.get_user_by_google_id(db, user_data.google_id)
    if existing:
        raise HTTPException(status_code=409, detail="User with this Google ID already exists")
    return user_service.create_user(db, user_data)


@router.get("/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def deactivate_user(user_id: UUID, db: Session = Depends(get_db)):
    if not user_service.deactivate_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
