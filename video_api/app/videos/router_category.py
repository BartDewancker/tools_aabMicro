from fastapi import APIRouter
from fastapi import status
from fastapi import Response, status
from typing import List

#from .mdb_repo_category import CategoryRepository
from .mdb_repo_category import CategoryRepository
from .models import Category, BaseResponse, NULL_OBJ
from viewmodels import CategoryViewModel

router = APIRouter()
repo = CategoryRepository

@router.get("/", tags=["Category"], name="Get all categories",
                      responses={status.HTTP_200_OK: {"model": List[CategoryViewModel]},
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
    

@router.get("/{item_id}", tags=["Category"], name="Get a category",
                                 responses={status.HTTP_200_OK: {"model": CategoryViewModel},
                                            status.HTTP_404_NOT_FOUND: {"model": str},
                                            status.HTTP_409_CONFLICT: {"model": str}})
def get_one(id: int, response: Response):
   
    res = BaseResponse(message="", error="")
    item = repo.get_one(res, id)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (item is not None):
        response.status_code = status.HTTP_200_OK
        return item
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message


@router.post("/", tags=["Category"], name="Insert a category",
                        responses={status.HTTP_201_CREATED: {"model": CategoryViewModel},
                                   status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
                                   status.HTTP_409_CONFLICT: {"model": str}})
def insert(item: Category, response: Response):
    
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
    

@router.put("/", tags=["Category"], name="Update a category",
                       responses={status.HTTP_200_OK: {"model": CategoryViewModel},
                                  status.HTTP_404_NOT_FOUND: {"model": str},
                                  status.HTTP_409_CONFLICT: {"model": str}})
def update(item: Category, response: Response):

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
    
@router.delete("/{item_id}", tags=["Category"], name="Delete a category",
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
