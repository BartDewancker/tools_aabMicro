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


