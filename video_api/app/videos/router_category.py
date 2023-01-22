from fastapi import APIRouter
from fastapi import status
from typing import List

from .repo_category import CategoryRepository
from .models import Category, CategoryResponse
from viewmodels import CategoryViewModel

router = APIRouter()

@router.get("/", tags=["Category"], name="Get all categories", response_model=List[CategoryViewModel])
def get_all():
    res = CategoryResponse(item=None, message="", error="")
    return CategoryRepository.get_all(res)
