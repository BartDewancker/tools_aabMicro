from pydantic import BaseModel
from typing import Optional, List
from videos.models import Video, Category, Library

class VideoViewModel(Video):
    category: Optional[Category]
    library: Optional[Library]

class CategoryViewModel(Category):
    videos: Optional[List[Video]]

class LibraryViewModel(Library):
    videos: Optional[List[Video]]