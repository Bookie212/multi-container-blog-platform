from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

# For creating posts (what user sends)
class BlogPostCreate(BaseModel):
    title: str
    content: str
    author: str

# For reading posts (what user receives)
class BlogPost(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
