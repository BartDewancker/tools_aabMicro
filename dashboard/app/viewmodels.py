from pydantic import BaseModel
from typing import Optional, List
from videos.models import Video, Category

NULL_OBJ = "Invalid object."

class VideoViewModel(Video):
    category: Category

class CategoryViewModel(Category):
    video: Optional[List[Video]]

class VideoResponse(BaseModel):
    item: Optional[Video]
    message: str
    error: Optional[str]

class CategorResponse(BaseModel):
    item: Optional[Category]
    message: str
    error: Optional[str]
   