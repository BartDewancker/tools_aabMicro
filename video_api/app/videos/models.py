from pydantic import BaseModel
from typing import Optional, List, Dict

NULL_OBJ = "Invalid object."

# *** Video ***
class BaseVideo(BaseModel):
    id: Optional[int]

class Video(BaseVideo):
    path: str
    category_id: int
    library_id: int
    annotation: str

    class Config:
        orm_mode = True

# *** Category ***
class BaseCategory(BaseModel):
    id: Optional[int]
        
class Category(BaseCategory):
    description: str
    
    class Config:
        orm_mode = True

# *** Library ***
class BaseLibrary(BaseModel):
    id: Optional[int]
        
class Library(BaseLibrary):
    description: str
    
    class Config:
        orm_mode = True

# *** Shared ***
class BaseResponse(BaseModel):
    message: str
    error: Optional[str]

class DeleteResponse(BaseModel):
    message: str