from typing import Optional, List, Union
import strawberry
from videos.models import Video, Category
from viewmodels import VideoViewModel, CategoryViewModel

# ******* Models *******
@strawberry.experimental.pydantic.type(model=Video, all_fields=True)
class VideoType:
    pass

@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class CategoryType:
    pass

@strawberry.experimental.pydantic.type(model=VideoViewModel, fields=['id', 'path'])
class VideoViewModelType:
    category: CategoryType

@strawberry.experimental.pydantic.type(model=CategoryViewModel, fields=['id', 'description'])
class CategoryViewModelType:
    videos: Optional[List[VideoType]]

# ******* Input types *******
@strawberry.input
class VideoInput(VideoType):
    pass

@strawberry.input
class CategoryInput(CategoryType):
    pass

# ******* Union types *******
@strawberry.type
class BaseMessage:
    message: str

@strawberry.type
class ListOfVideos():
    videos: List[VideoViewModelType]

@strawberry.type
class ListOfCategories():
    categories: List[CategoryViewModelType]

VideoReturn = strawberry.union(
    "VideoReturn", [VideoViewModelType, BaseMessage]
)

CategoryReturn = strawberry.union(
    "CategoryReturn", [CategoryViewModelType, BaseMessage]
)


