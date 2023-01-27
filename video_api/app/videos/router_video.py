from fastapi import APIRouter
from fastapi import status
from fastapi import Response, status
from typing import List
from nosql_database import MONGO_DATABASE_ON

if MONGO_DATABASE_ON == "ON":
    from .mdb_repo_video import VideoRepository
else:
    from .repo_video import VideoRepository

from .models import Video, BaseResponse, NULL_OBJ
from viewmodels import VideoViewModel

router = APIRouter()
router2 = APIRouter()
repo = VideoRepository

@router.get("/", tags=["Video"], name="Get all videos",
                      responses={status.HTTP_200_OK: {"model": List[VideoViewModel]},
                                 status.HTTP_404_NOT_FOUND: {"model": str},
                                 status.HTTP_409_CONFLICT: {"model": str}})
def get_all(response: Response):
    res = BaseResponse(message="", error="")

    items = repo.get_all(res)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (items is not None and len(items) > 0):
        response.status_code = status.HTTP_200_OK
        return items
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
     
@router.get("/{item_id}", tags=["Video"], name="Get a video",
                                 responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                            status.HTTP_404_NOT_FOUND: {"model": str},
                                            status.HTTP_409_CONFLICT: {"model": str}})
def get_one(id: int, response: Response):
   
    res = BaseResponse(message="", error="")
    item = repo.get_one(res, id=id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (item is not None):
        response.status_code = status.HTTP_200_OK
        return item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message


@router.post("/", tags=["Video"], name="Insert a video",
                        responses={status.HTTP_201_CREATED: {"model": VideoViewModel},
                                   status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
                                   status.HTTP_409_CONFLICT: {"model": str}})
def insert(item: Video, response: Response):
    
    res = BaseResponse(message="", error="")
    added_item = repo.insert(res, item)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif(res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (added_item is not None):
        response.status_code = status.HTTP_201_CREATED
        return added_item
   
       
@router.put("/", tags=["Video"], name="Update a video",
                       responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                  status.HTTP_404_NOT_FOUND: {"model": str},
                                  status.HTTP_409_CONFLICT: {"model": str}})
def update(item: Video, response: Response):

    res = BaseResponse(message="", error="")
    updated_item = repo.update(res, item)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (updated_item is not None):
        response.status_code = status.HTTP_200_OK
        print(res.message)
        return updated_item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    
@router.put("/{item_id},{item_path}", tags=["Video"], name="Update a video path",
                       responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                  status.HTTP_404_NOT_FOUND: {"model": str},
                                  status.HTTP_409_CONFLICT: {"model": str}})
def update_path(id: int, path: str, response: Response):

    res = BaseResponse(message="", error="")
    updated_item = repo.updatePath(res, id, path)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (updated_item is not None):
        response.status_code = status.HTTP_200_OK
        return updated_item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message

@router.delete("/{item_id}", tags=["Video"], name="Delete a video",
                                    responses={status.HTTP_200_OK: {"model": str},
                                               status.HTTP_404_NOT_FOUND: {"model": str},
                                               status.HTTP_409_CONFLICT: {"model": str}})
def delete(id: int, response: Response):
   
    res = BaseResponse(message="", error="")
    num_rows_deleted = repo.delete(res, id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (num_rows_deleted > 0):
        response.status_code = status.HTTP_200_OK
        return res.message
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    
@router2.get("/{item_category_id}", tags=["Video"], name="Get all videos in a category",
                                 responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                            status.HTTP_404_NOT_FOUND: {"model": str},
                                            status.HTTP_409_CONFLICT: {"model": str}})
def get_many(category_id: int, response: Response):
   
    res = BaseResponse(message="", error="")
    item = repo.get_many(res, category_id=category_id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (item is not None):
        response.status_code = status.HTTP_200_OK
        return item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    
@router2.put("/{item_id},{item_annotation}", tags=["Video"], name="Update a video annotation",
                       responses={status.HTTP_200_OK: {"model": VideoViewModel},
                                  status.HTTP_404_NOT_FOUND: {"model": str},
                                  status.HTTP_409_CONFLICT: {"model": str}})
def update_path(id: int, annotation: str, response: Response):

    res = BaseResponse(message="", error="")
    updated_item = repo.updateAnnotation(res, id, annotation)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return res.message
    elif (updated_item is not None):
        response.status_code = status.HTTP_200_OK
        return updated_item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
    