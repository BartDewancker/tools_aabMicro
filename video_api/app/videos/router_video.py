from fastapi import APIRouter
from fastapi import status
from fastapi import Response, status
from typing import List

from .repo_video import VideoRepository
from .models import Video, VideoResponse, NULL_OBJ
from viewmodels import VideoViewModel

router = APIRouter()

@router.get("/", tags=["Video"], name="Get all videos",
                      responses={status.HTTP_200_OK: {"model": List[VideoViewModel]},
                                 status.HTTP_404_NOT_FOUND: {"model": str},
                                 status.HTTP_409_CONFLICT: {"model": str}})
def get_all(response: Response):
    res = VideoResponse(message="", error="")

    videos = VideoRepository.get_all(res)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (videos is not None and len(videos) > 0):
        response.status_code = status.HTTP_200_OK
        return videos
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
     
@router.get("/{video_id}", tags=["Video"], name="Get a video",
                                 responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                            status.HTTP_404_NOT_FOUND: {"model": str},
                                            status.HTTP_409_CONFLICT: {"model": str}})
def get_one(video_id: int, response: Response):
   
    res = VideoResponse(message="", error="")
    video = VideoRepository.get_one(res, id=video_id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (video is not None):
        response.status_code = status.HTTP_200_OK
        return video
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    

@router.post("/", tags=["Video"], name="Insert a video",
                        responses={status.HTTP_201_CREATED: {"model": VideoViewModel},
                                   status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
                                   status.HTTP_409_CONFLICT: {"model": str}})
def insert_video(video: Video, response: Response):
    
    res = VideoResponse(message="", error="")
    added_video = VideoRepository.insert(res, video)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif(res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (added_video is not None):
        response.status_code = status.HTTP_201_CREATED
        return added_video
   
       
@router.put("/", tags=["Video"], name="Update a vdeo",
                       responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                  status.HTTP_404_NOT_FOUND: {"model": str},
                                  status.HTTP_409_CONFLICT: {"model": str}})
def update_video(video: Video, response: Response):

    res = VideoResponse(message="", error="")
    updated_video = VideoRepository.update(res, video)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (updated_video is not None):
        response.status_code = status.HTTP_200_OK
        print(res.message)
        return updated_video
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
  

@router.delete("/{video_id}", tags=["Video"], name="Delete a video",
                                    responses={status.HTTP_200_OK: {"model": str},
                                               status.HTTP_404_NOT_FOUND: {"model": str},
                                               status.HTTP_409_CONFLICT: {"model": str}})
def delete_video(video_id: int, response: Response):
   
    res = VideoResponse(message="", error="")
    num_rows_deleted = VideoRepository.delete(res, video_id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (num_rows_deleted > 0):
        response.status_code = status.HTTP_200_OK
        return res.message
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    