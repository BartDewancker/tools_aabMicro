from fastapi import APIRouter
from fastapi import status
from .repository import SubjectRepository
from viewmodels import SubjectResponse, NULL_OBJ
from fastapi.responses import Response
from .models import Subject
router = APIRouter()

@router.post("/", tags=["Subjects"], name="Create a subject", response_model=str)
def create_subject(subject: Subject):
    result = SubjectRepository.create(subject)
    return result

@router.put("/", tags=["Subjects"], name="Update a subject")
def update_subject(subject: Subject, response: Response):

    res = SubjectResponse(item=None, message="", error="")
    updated_subject = SubjectRepository.update(subject, res)

    if res.error != "":
        response.status_code = status.HTTP_409_CONFLICT
    elif (res.message == NULL_OBJ):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif (res is not None):
        response.status_code = status.HTTP_201_CREATED
        res.item = updated_subject
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
  
    return res