from utils import get_uuid
from typing import List
from nosql_database import (
    get_database
)

from viewmodels import VideoViewModel
from .models import Video, Category, Library, BaseResponse, NULL_OBJ
import traceback
import json

videos = get_database('videos')
categories = get_database('categories')
libraries = get_database('libraries')

class VideoRepository():
    
    @staticmethod
    def get_all(response: BaseResponse) -> List[VideoViewModel]:
        try:
            db_objects = videos.find()
            if db_objects is not None:
                videoList = []
                for document in db_objects:
                    
                    # Convert in document the annotation field from json format to string.
                    document['annotation'] = json.dumps(document['annotation'])
                    video_obj = VideoViewModel(**document)
                    
                    cat = categories.find_one({'id': document['category_id']})
                    if cat:
                        video_obj.category = Category(**cat)

                    lib = libraries.find_one({'id': document['library_id']})
                    if lib:
                        video_obj.library = Library(**lib)
                    videoList.append(video_obj)
                return videoList
            else:
                response.message = f"No object of type {Video} were found in the database!"
                return None
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
   
    @staticmethod
    def get_one(response: BaseResponse, **kwargs) -> VideoViewModel:
        try:
            keyIn = ""
            valueIn = ""

            for(key, value) in kwargs.items():
                keyIn = key
                valueIn = value

            print(f"key= {keyIn}, value= {valueIn}")
            if(keyIn == "" or valueIn == ""):
                response.message = "Invalid arguments."
                return None
            
            document = videos.find_one(kwargs)
            if document is not None:

                # Convert in document the annotation field from json format to string.
                document['annotation'] = json.dumps(document['annotation'])
                obj = VideoViewModel(**document)
                cat = categories.find_one({'id': document['category_id']})
                if cat:
                    obj.category = Category(**cat)

                lib = libraries.find_one({'id': document['library_id']})
                if lib:
                    obj.library = Library(**lib)

                response.message = f"Found item with id '{obj.id}'"
                return obj
            else:
                response.message = f"No item found for {keyIn} with value '{valueIn}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
           
    
    @staticmethod
    def get_many(response: BaseResponse, **kwargs) -> List[VideoViewModel]:
        try:
            db_objects = videos.find(kwargs)
            if db_objects is not None:
                videoList = []
                for document in db_objects:

                    # Convert in document the annotation field from json format to string.
                    document['annotation'] = json.dumps(document['annotation'])
                    video_obj = VideoViewModel(**document)
                   
                    cat = categories.find_one({'id': document['category_id']})
                    if cat:
                        video_obj.category = Category(**cat)

                    lib = libraries.find_one({'id': document['library_id']})
                    if lib:
                        video_obj.library = Library(**lib)
                    videoList.append(video_obj)
                return videoList
            else:
                response.message = f"No object of type {Video} were found in the database!"
                return None
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            
