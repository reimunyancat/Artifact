from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date

class Input(BaseModel):
    artist_name: str

class Music(BaseModel):
    name: str
    publish_date: date
    music_link: Optional[HttpUrl] = None  
    album_name: Optional[str] = None
    genre: Optional[str] = None

class Artist(BaseModel):
    artist_name: str
    introduction: str
    feature: List[str]
    musics: List[Music]
