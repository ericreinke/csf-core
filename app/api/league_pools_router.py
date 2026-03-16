from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.league_pool import LeaguePoolCreate, LeaguePoolUpdate, LeaguePoolResponse
from app.services import league_pool_service, league_service

router = APIRouter(prefix="/leagues", tags=["League Pools"])


@router.post("/{league_id}/pools", response_model=LeaguePoolResponse, status_code=201)
def create_pool(league_id: UUID, pool_data: LeaguePoolCreate, db: Session = Depends(get_db)):
    if pool_data.league_id != league_id:
        raise HTTPException(status_code=400, detail="Path league_id and body league_id must match")
        
    league = league_service.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    return league_pool_service.create_pool(db, pool_data)


@router.get("/{league_id}/pools", response_model=list[LeaguePoolResponse])
def get_pools(league_id: UUID, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    league = league_service.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
        
    return league_pool_service.get_pools_by_league(db, league_id, skip=skip, limit=limit)


@router.get("/{league_id}/pools/{pool_id}", response_model=LeaguePoolResponse)
def get_pool(league_id: UUID, pool_id: UUID, db: Session = Depends(get_db)):
    pool = league_pool_service.get_pool(db, pool_id)
    if not pool or pool.league_id != league_id:
        raise HTTPException(status_code=404, detail="Pool not found in this league")
    return pool


@router.patch("/{league_id}/pools/{pool_id}", response_model=LeaguePoolResponse)
def update_pool(league_id: UUID, pool_id: UUID, pool_data: LeaguePoolUpdate, db: Session = Depends(get_db)):
    pool = league_pool_service.get_pool(db, pool_id)
    if not pool or pool.league_id != league_id:
        raise HTTPException(status_code=404, detail="Pool not found in this league")
        
    return league_pool_service.update_pool(db, pool_id, pool_data)


@router.delete("/{league_id}/pools/{pool_id}", status_code=204)
def delete_pool(league_id: UUID, pool_id: UUID, db: Session = Depends(get_db)):
    pool = league_pool_service.get_pool(db, pool_id)
    if not pool or pool.league_id != league_id:
        raise HTTPException(status_code=404, detail="Pool not found in this league")
        
    league_pool_service.delete_pool(db, pool_id)
