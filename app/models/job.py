from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class JobListing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(unique=True, index=True)
    title: str
    company: str
    location: str
    description: str
    url: str
    source_api: str = "Adzuna"
    created_at: datetime = Field(default_factory=datetime.utcnow)