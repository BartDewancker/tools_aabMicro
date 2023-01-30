from utils import get_uuid
from typing import List
from nosql_database import (
    get_database
)

from viewmodels import CategoryViewModel
from .models import Category, BaseResponse, Video, NULL_OBJ
import traceback
import json

categories = get_database('categories')
videos = get_database('videos')

class CategoryRepository():
    
    @staticmethod
    def get_all(response: BaseResponse) -> List[CategoryViewModel]:
        try:
            documents = categories.find()
            if documents is not None:
                categoryList = []
                for doc in documents:
                    
                    cat_obj = CategoryViewModel(**doc)
                    cat_videos = videos.find({'category_id': doc['id']})

                    for video in cat_videos:
                        video['annotation'] = json.dumps(video['annotation'])
                        cat_obj.videos.append(Video(**video))

                    categoryList.append(cat_obj)
                
                return categoryList
            else:
                response.message = f"No object of type {Category} were found in the database!"
                return None        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = err.__doc__
            #response.error = "Database error! Call the database administrator"

    
    @staticmethod
    def get_one(response: BaseResponse, idGet: int) -> CategoryViewModel:
        try:
            document = categories.find_one({'id': idGet})
            if document is not None:
                obj = CategoryViewModel(**document)

                cat_videos = videos.find({'category_id': document['id']})
                for video in cat_videos:
                    video['annotation'] = json.dumps(video['annotation'])
                    obj.videos.append(Video(**video))

                response.message = f"Found item with id '{obj.id}'"
                return obj
            else:
                response.message = f"No item found for with _id '{idGet}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
