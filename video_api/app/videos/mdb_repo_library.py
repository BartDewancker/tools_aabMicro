from utils import get_uuid
from typing import List
from nosql_database import (
    get_database
)

from viewmodels import LibraryViewModel
from .models import Library, BaseResponse, Video, NULL_OBJ
import traceback
import json

libraries = get_database('libraries')
videos = get_database('videos')

class LibraryRepository():
    
    @staticmethod
    def get_all(response: BaseResponse) -> LibraryViewModel:
        try:
            documents = libraries.find()
            if documents is not None:
                libraryList = []
                for doc in documents:

                    lib_obj = LibraryViewModel(**doc)
                    lib_videos = videos.find({'library_id': doc['id']})

                    for video in lib_videos:
                        video['annotation'] = json.dumps(video['annotation'])
                        lib_obj.videos.append(Video(**video))

                    libraryList.append(lib_obj)

                return libraryList
            else:
                response.message = f"No object of type {Library} were found in the database!"
                return None        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            #response.error = err.__doc__
            response.error = "Database error! Call the database administrator"


    @staticmethod
    def get_one(response: BaseResponse, idGet: int) -> LibraryViewModel:
        try:
            document = libraries.find_one({'id': idGet})
            if document is not None:
                obj = LibraryViewModel(**document)

                lib_videos = videos.find({'library_id': document['id']})
                for video in lib_videos:
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


    @staticmethod
    def insert(response: BaseResponse, new_item: Library):
        try:
            if new_item is None:
                response.message = NULL_OBJ
                return None
            else:
                document = new_item.dict()
                document["_id"] = get_uuid()
                document["videos"] = []

                all_objects = LibraryRepository.get_all(response)

                if all_objects is not None:
                    document["id"] = len(LibraryRepository.get_all(response)) + 1
                else:
                    document["id"] = 1

                result = libraries.insert_one(document)
                assert result.acknowledged
                return LibraryRepository.get_one(response, document["id"])
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"


    @staticmethod
    def update(response: BaseResponse, new_obj: Library):
        try:
            if new_obj is None:
                response.message = NULL_OBJ
                return None
            else:
                document = new_obj.dict()
                result = libraries.replace_one({"id": new_obj.id}, document)

                if result.matched_count == 1:                  
                    return LibraryRepository.get_one(response, document["id"])
                else:
                    response.message = f"No item found with id '{new_obj.id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"


    @staticmethod
    def delete(response: BaseResponse, idDel: int):
        try:
            result = libraries.delete_one({"id": idDel})
            if result.deleted_count == 1:
                response.message = f"Deleted item with id '{idDel}'"
            elif result.deleted_count == 0:
                response.message = f"No item found with id '{idDel}'"
            return result.deleted_count
        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"

