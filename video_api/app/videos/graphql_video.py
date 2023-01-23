from typing import Optional, List, Union
import strawberry

from .repo_video import VideoRepository
from .models import Video, BaseResponse, NULL_OBJ
from graphql_models import VideoInput, VideoType, VideoViewModelType, ListOfVideos, BaseMessage, VideoReturn

@strawberry.type
class Query:
      
    @strawberry.field
    def video_get_all(self) -> Union[ListOfVideos, BaseMessage]:
      
        res = BaseResponse(message="", error="")
        items: List[VideoType] = VideoRepository.get_all(res)
        
        if res.error != "":
            return BaseMessage(message = res.error)
        elif (items is not None and len(items) > 0):
            return ListOfVideos(videos=items)
        else:
            return BaseMessage(message = res.message)
    
    @strawberry.field
    def video_get_one(self, path: Optional[str] = strawberry.UNSET, id: Optional[int] = strawberry.UNSET) -> VideoReturn:
        res = BaseResponse(message="", error="")

        if (path is not strawberry.UNSET):
            item = VideoRepository.get_one(res, path=path)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (item is not None):
                print(res.message)
                return item
            else:
                return BaseMessage(message = res.message)
        elif (id is not strawberry.UNSET):
            item = VideoRepository.get_one(res, id=id)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (item is not None):
                print(res.message)
                return item
            else:
                return BaseMessage(message = res.message)
            
    @strawberry.field
    def video_get_by_category_id(self, id: int = strawberry.UNSET) -> Union[ListOfVideos, BaseMessage]:
        res = BaseResponse(message="", error="")

        if (id is not strawberry.UNSET):
            items: List[VideoType] = VideoRepository.get_many(res, category_id=id)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (items is not None):
                print(res.message)
                return ListOfVideos(videos=items)
            else:
                return BaseMessage(message = res.message)
     
@strawberry.type
class Mutation:
    @strawberry.mutation
    def video_insert(self, item: VideoInput) -> VideoReturn:
   
        res = BaseResponse(message="", error="")
        added_item = VideoRepository.insert(res, Video(**item.__dict__))

        if res.error != "":
            return BaseMessage(message = res.error)
        elif(res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (added_item is not None):
            return added_item
        
    @strawberry.mutation
    def video_update(self, item: VideoInput) -> VideoReturn:
   
        res = BaseResponse(message="", error="")
        updated_item = VideoRepository.update(res, Video(**item.__dict__))

        if res.error != "":
            return  BaseMessage(message = res.error)
        elif (res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (updated_item is not None):
            print(res.message)
            return updated_item
        else:
            return BaseMessage(message = res.message)
        
    @strawberry.mutation
    def video_updatePath(self, id: int, path: str) -> VideoReturn:
   
        res = BaseResponse(message="", error="")
        updated_item = VideoRepository.updatePath(res, id, path)

        if res.error != "":
            return  BaseMessage(message = res.error)
        elif (updated_item is not None):
            return updated_item
        else:
            return BaseMessage(message = res.message)
        
    @strawberry.mutation
    def video_updateAnnotation(self, id: int, annotation: str) -> VideoReturn:
   
        res = BaseResponse(message="", error="")
        updated_item = VideoRepository.updateAnnotation(res, id, annotation)

        if res.error != "":
            return  BaseMessage(message = res.error)
        elif (updated_item is not None):
            return updated_item
        else:
            return BaseMessage(message = res.message)
        
    @strawberry.mutation
    def video_delete(self, id: int = strawberry.UNSET) -> str:
   
        res = BaseResponse(message="", error="")
        num_rows_deleted = VideoRepository.delete(res, id)

        if res.error != "":
            return res.error
        elif (num_rows_deleted > 0):
            return res.message
        else:
            return res.message
        
        
        
       