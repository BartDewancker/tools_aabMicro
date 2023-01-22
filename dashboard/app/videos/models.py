from pydantic import BaseModel
from typing import Optional

NULL_OBJ = "Invalid object."

class BaseVideo(BaseModel):
    id: Optional[int]

class Video(BaseVideo):
    path: str
    category_id: int

    class Config:
        orm_mode = True

class VideoResponse(BaseModel):
    message: str
    error: Optional[str]

class BaseCategory(BaseModel):
    id: Optional[int]
        
class Category(BaseCategory):
    description: str
    
    class Config:
        orm_mode = True

class CategoryResponse(BaseModel):
    message: str
    error: Optional[str]