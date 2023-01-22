from pydantic import BaseModel
from typing import Optional, List
from videos.models import Video, Category

class VideoViewModel(Video):
    category: Category

class CategoryViewModel(Category):
    videos: Optional[List[Video]]

   