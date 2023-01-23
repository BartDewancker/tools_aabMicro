from typing import Optional, List, Union
import strawberry

from .repo_video import VideoRepository
from .models import Video, BaseResponse, NULL_OBJ
from graphql_models import VideoInput, VideoType, VideoViewModelType, ListOfVideos, BaseMessage, VideoReturn

@strawberry.type
class Query:
      
    @strawberry.field
    def get_all_videos(self) -> Union[ListOfVideos, BaseMessage]:
      
        res = BaseResponse(message="", error="")
        videos: List[VideoType] = VideoRepository.get_all(res)
        
        if res.error != "":
            return BaseMessage(message = res.error)
        elif (videos is not None and len(videos) > 0):
            return ListOfVideos(videos=videos)
        else:
            return BaseMessage(message = res.message)
    
    @strawberry.field
    def get_one_video(self, pathIn: Optional[str] = strawberry.UNSET, idIn: Optional[int] = strawberry.UNSET) -> VideoReturn:
        res = BaseResponse(message="", error="")

        if (pathIn is not strawberry.UNSET):
            video = VideoRepository.get_one(res, path=pathIn)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (video is not None):
                print(res.message)
                return video
            else:
                return BaseMessage(message = res.message)
        elif (idIn is not strawberry.UNSET):
            video = VideoRepository.get_one(res, id=idIn)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (video is not None):
                print(res.message)
                return video
            else:
                return BaseMessage(message = res.message)
            
    @strawberry.field
    def get_videos_by_category_id(self, id: int = strawberry.UNSET) -> Union[ListOfVideos, BaseMessage]:
        res = BaseResponse(message="", error="")

        if (id is not strawberry.UNSET):
            videos: List[VideoType] = VideoRepository.get_many(res, category_id=id)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (videos is not None):
                print(res.message)
                return ListOfVideos(videos=videos)
            else:
                return BaseMessage(message = res.message)
     
@strawberry.type
class Mutation:
    @strawberry.mutation
    def insert_video(self, video: VideoInput) -> VideoReturn:
   
        res = BaseResponse(message="", error="")
        added_video = VideoRepository.insert(Video(res, **video.__dict__))

        if res.error != "":
            return BaseMessage(message = res.error)
        elif(res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (added_video is not None):
            return added_video
        
    @strawberry.mutation
    def delete_video(self, id: int = strawberry.UNSET) -> str:
   
        res = BaseResponse(message="", error="")
        num_rows_deleted = VideoRepository.delete(res, id)

        if res.error != "":
            return res.error
        elif (num_rows_deleted > 0):
            return res.message
        else:
            return res.message
        
        
        
       