from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/admin", tags=["admin"])

# Pydantic Models

class User(BaseModel):
    id: int
    email: str
    join_date: str = Field(..., description="Date user joined (YYYY-MM-DD)")
    listen_time: int = Field(..., description="Total listen time in minutes")

class UsersResponse(BaseModel):
    data: List[User]
    meta: dict

class Podcast(BaseModel):
    id: int
    title: str
    publisher: str
    episode_count: int
    total_listens: int

class PodcastsResponse(BaseModel):
    data: List[Podcast]
    meta: dict

class Episode(BaseModel):
    id: int
    title: str
    podcast_id: int
    listen_count: int

class EpisodesResponse(BaseModel):
    data: List[Episode]
    meta: dict


# Routes

@router.get("/dashboard")
async def get_admin_dashboard():
    """
    Get summary dashboard data:
    - user count
    - active podcasts
    - site uptime (days)
    """
    return {
        "message": "Welcome Admin",
        "user_count": 1234,
        "active_podcasts": 567,
        "site_uptime_days": 99.5,
    }


@router.get("/users", response_model=UsersResponse)
async def list_users(
    limit: int = Query(20, ge=1, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    active: Optional[bool] = Query(None, description="Filter by active users"),
    joined_after: Optional[str] = Query(None, description="Filter users joined after this date (YYYY-MM-DD)"),
):
    """
    Return a list of recent registered users with basic info.
    Supports optional filtering and pagination.
    """
    # Dummy static data for now
    users = [
        User(id=1, email="user1@example.com", join_date="2025-05-01", listen_time=120),
        User(id=2, email="user2@example.com", join_date="2025-05-10", listen_time=300),
    ]
    return UsersResponse(data=users, meta={"total": len(users), "limit": limit, "offset": offset})


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Get user details by ID.
    """
    return User(id=user_id, email=f"user{user_id}@example.com", join_date="2025-05-01", listen_time=1234)


@router.get("/podcasts", response_model=PodcastsResponse)
async def list_podcasts(
    limit: int = Query(20, ge=1, description="Number of podcasts to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    popular: Optional[bool] = Query(None, description="Filter by popular podcasts"),
    category: Optional[str] = Query(None, description="Filter by podcast category"),
):
    """
    List active podcasts with optional filters and pagination.
    """
    podcasts = [
        Podcast(id=101, title="Podverse Daily", publisher="Podverse Studios", episode_count=125, total_listens=12345),
        Podcast(id=102, title="Tech Talk", publisher="Tech Media", episode_count=80, total_listens=6789),
    ]
    return PodcastsResponse(data=podcasts, meta={"total": len(podcasts), "limit": limit, "offset": offset})


@router.get("/podcasts/{podcast_id}", response_model=Podcast)
async def get_podcast(podcast_id: int):
    """
    Get podcast detail and stats by ID.
    """
    return Podcast(
        id=podcast_id,
        title=f"Podcast {podcast_id}",
        publisher="Sample Publisher",
        episode_count=42,
        total_listens=5000,
    )


@router.get("/podcasts/{podcast_id}/episodes", response_model=EpisodesResponse)
async def list_episodes(
    podcast_id: int,
    limit: int = Query(20, ge=1, description="Number of episodes to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """
    List episodes for a specific podcast.
    """
    episodes = [
        Episode(id=1001, title="Episode 1: Welcome", podcast_id=podcast_id, listen_count=1000),
        Episode(id=1002, title="Episode 2: Deep Dive", podcast_id=podcast_id, listen_count=850),
    ]
    return EpisodesResponse(data=episodes, meta={"total": len(episodes), "limit": limit, "offset": offset})


@router.get("/episodes/{episode_id}", response_model=Episode)
async def get_episode(episode_id: int):
    """
    Get episode detail and stats by ID.
    """
    return Episode(id=episode_id, title=f"Episode {episode_id}", podcast_id=101, listen_count=1500)


@router.get("/stats/listening-trends")
async def listening_trends(
    start_date: Optional[str] = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter end date (YYYY-MM-DD)"),
    podcast_id: Optional[int] = Query(None, description="Filter by podcast ID"),
    episode_id: Optional[int] = Query(None, description="Filter by episode ID"),
):
    """
    Return podcast listening trends over time.
    """
    return {
        "dates": ["2025-05-01", "2025-05-02", "2025-05-03"],
        "listens": [100, 120, 95],
    }


@router.get("/site-uptime")
async def site_uptime():
    """
    Return uptime statistics for the platform.
    """
    return {
        "uptime_days": 99.5,
        "last_downtime": "2025-04-30T14:00:00Z",
        "downtime_duration_minutes": 15,
    }
