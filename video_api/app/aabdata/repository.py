from typing import List
from viewmodels import SubjectResponse, NULL_OBJ
from uuid import uuid4
from nosql_database import (
    get_database
)
from .models import Subject
from fastapi.responses import Response
import traceback
collection = get_database('subjects')

class SubjectRepository():

    @staticmethod
    def get_all() -> List[Subject]:
        try:
            subjects = collection.find()
            return [Subject(**document) for document in subjects]
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            return []

    @staticmethod
    def create(subject: Subject) -> str:
        """Create a new subject"""
        document = subject.dict()
        document["_id"] = str(uuid4())
        result = collection.insert_one(document)
        assert result.acknowledged
        return "Created"
    
    @staticmethod
    def update(subject: Subject, response: SubjectResponse):
        try:
            if subject is None:
                response.message = NULL_OBJ
                return None
            else:
                old_obj = collection.find( { "_id": subject._id } )

                if old_obj is not None:
                                 
                    result = collection.update_one( { "_id": subject._id }, { "$set": { "title": subject.title } } )

                    if result.matched_count == 0:
                        response.message = f"Subject with id '{subject._id}' not updated" 
                        return None
                    else:
                        response.message = f"Subjes with id '{subject._id}' updated title '{subject.title}'"                   
                        return collection.find( { "_id": subject._id } )
                else:
                    response.message = f"No item found with id '{subject._id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)