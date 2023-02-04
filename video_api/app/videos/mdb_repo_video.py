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

                    video_obj.annotation = json.loads(video_obj.annotation)
                    
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

                obj.annotation = json.loads(obj.annotation)

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

                    video_obj.annotation = json.loads(video_obj.annotation)
                   
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
    def insert(response: BaseResponse, new_item: Video) -> VideoViewModel:
        try:
            if new_item is None:
                response.message = NULL_OBJ
                return None
            else:
                document = new_item.dict()
                document["_id"] = get_uuid()

                # Convert in document the annotation field from string to json format.
                document['annotation'] = json.loads(document['annotation'])

                all_objects = VideoRepository.get_all(response)

                if all_objects is not None:
                    document["id"] = len(VideoRepository.get_all(response)) + 1
                else:
                    document["id"] = 1

                result = videos.insert_one(document)
                assert result.acknowledged
                return VideoRepository.get_one(response, id=document["id"])
              
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            

    @staticmethod
    def update(response: BaseResponse, new_obj: Video) -> VideoViewModel:
        try:
            if new_obj is None:
                response.message = NULL_OBJ
                return None
            else:
                document = new_obj.dict()

                # Convert in document the annotation field from string to json format.
                document['annotation'] = json.loads(document['annotation'])

                result = videos.replace_one({"id": new_obj.id}, document)

                if result.matched_count == 1:
                    return VideoRepository.get_one(response, id=new_obj.id)
                else:
                    response.message = f"No item found with id '{new_obj.id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
        

    @staticmethod
    def updatePath(response: BaseResponse, id: int, new_path: str) -> VideoViewModel:
        try:
            document = videos.find_one({"id": id})

            if document is not None:
                document.update({"path": new_path})
                result = videos.replace_one({"id": id}, document)
                if result.matched_count == 1:
                    return VideoRepository.get_one(response, id=id)
                else:
                    response.message = f"No item updated with id '{id}'"
                    return None
            else:
                response.message = f"No item found with id '{id}'"
                return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"

    
    @staticmethod
    def updateAnnotation(response: BaseResponse, id: int, new_annotation: str) -> VideoViewModel:
        try:
            document = videos.find_one({"id": id})

            if document is not None:
                
                # Convert the new annotation from string to json format.  
                document['annotation'] = json.loads(new_annotation)

                result = videos.replace_one({"id": id}, document)
                if result.matched_count == 1:
                    return VideoRepository.get_one(response, id=id)
                else:
                    response.message = f"No item updated with id '{id}'"
                    return None
            else:
                response.message = f"No item found with id '{id}'"
                return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"

           
    @staticmethod
    def delete(response: BaseResponse, idDel: int) -> str:
        try:
            result = videos.delete_one({"id": idDel})
            if result.deleted_count == 1:
                response.message = f"Deleted item with id '{idDel}'"
            elif result.deleted_count == 0:
                response.message = f"No item found with id '{idDel}'"
            return result.deleted_count
        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"

    
    @staticmethod
    def updateCategoryID(response: BaseResponse, id: int, new_ID: int) -> VideoViewModel:
        try:
            document = videos.find_one({"id": id})

            if document is not None:

                document.update({"category_id": new_ID})
                
                result = videos.replace_one({"id": id}, document)
                if result.matched_count == 1:
                    return VideoRepository.get_one(response, id=id)
                else:
                    response.message = f"No item updated with id '{id}'"
                    return None
            else:
                response.message = f"No item found with id '{id}'"
                return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"