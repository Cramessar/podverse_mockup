from pydantic import BaseModel

class PodcastBase(BaseModel):
    title: str
    publisher: str
    category: str

class PodcastCreate(PodcastBase):
    pass

class Podcast(PodcastBase):
    id: int

    class Config:
        orm_mode = True
