from fastapi import APIRouter
from fastapi import status
from fastapi import Response, status
from typing import List

from .repo_category import CategoryRepository
from .models import Category, CategoryResponse
from viewmodels import CategoryViewModel

router = APIRouter()

@router.get("/", tags=["Category"], name="Get all categories",
                      responses={status.HTTP_200_OK: {"model": List[CategoryViewModel]},
                                 status.HTTP_404_NOT_FOUND: {"model": str},
                                 status.HTTP_409_CONFLICT: {"model": str}})
def get_all(response: Response):
    res = CategoryResponse(message="", error="")

    categories = CategoryRepository.get_all(res)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
        return res.error
    elif (categories is not None and len(categories) > 0):
        response.status_code = status.HTTP_200_OK
        return categories
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return res.message
