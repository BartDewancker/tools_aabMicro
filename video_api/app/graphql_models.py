from typing import Optional, List, Union
import strawberry
from videos.models import Video, Category, Library
from viewmodels import VideoViewModel, CategoryViewModel, LibraryViewModel

# ******* Models *******
@strawberry.experimental.pydantic.type(model=Video, all_fields=True)
class VideoType:
    pass

@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class CategoryType:
    pass

@strawberry.experimental.pydantic.type(model=Library, all_fields=True)
class LibraryType:
    pass

@strawberry.experimental.pydantic.type(model=VideoViewModel, fields=['id', 'path', 'annotation'])
class VideoViewModelType:
    category: CategoryType
    library: LibraryType

@strawberry.experimental.pydantic.type(model=CategoryViewModel, fields=['id', 'description'])
class CategoryViewModelType:
    videos: Optional[List[VideoType]]

@strawberry.experimental.pydantic.type(model=LibraryViewModel, fields=['id', 'description'])
class LibraryViewModelType:
    videos: Optional[List[VideoType]]

# ******* Input types *******
@strawberry.input
class VideoInput(VideoType):
    pass

@strawberry.input
class CategoryInput(CategoryType):
    pass

@strawberry.input
class LibraryInput(LibraryType):
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

@strawberry.type
class ListOfLibraries():
    categories: List[LibraryViewModelType]

VideoReturn = strawberry.union(
    "VideoReturn", [VideoViewModelType, BaseMessage]
)

CategoryReturn = strawberry.union(
    "CategoryReturn", [CategoryViewModelType, BaseMessage]
)

LibraryReturn = strawberry.union(
    "LibraryReturn", [LibraryViewModelType, BaseMessage]
)


