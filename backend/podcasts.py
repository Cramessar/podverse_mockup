from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import models, schemas, database

router = APIRouter(prefix="/podcasts", tags=["podcasts"])

@router.post("/", response_model=schemas.Podcast)
async def create_podcast(podcast: schemas.PodcastCreate, db: AsyncSession = Depends(database.get_db)):
    new_podcast = models.Podcast(**podcast.dict())
    db.add(new_podcast)
    await db.commit()
    await db.refresh(new_podcast)
    return new_podcast

@router.get("/", response_model=List[schemas.Podcast])
async def read_podcasts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        models.Podcast.__table__.select().offset(skip).limit(limit)
    )
    podcasts = result.scalars().all()
    return podcasts
