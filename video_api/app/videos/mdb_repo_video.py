from utils import get_uuid
from nosql_database import (
    get_database
)

from viewmodels import VideoViewModel
from .models import Video, Category, Library, BaseResponse, NULL_OBJ
import traceback

videos = get_database('videos')
categories = get_database('categories')
libraries = get_database('libraries')

class VideoRepository():
    
    @staticmethod
    def get_all(response: BaseResponse) -> VideoViewModel:
        try:
            db_objects = videos.find()
            if db_objects is not None:
                videoList = []
                for video in db_objects:
                    video_obj = VideoViewModel(**video)
                    
                    cat = categories.find_one({'id': video['category_id']})
                    if cat:
                        video_obj.category = Category(**cat)

                    lib = libraries.find_one({'id': video['library_id']})
                    if lib:
                        video_obj.library = Library(**lib)
                    videoList.append(video_obj)
                return videoList
            else:
                response.message = f"No object of type {Video} were found in the database!"
                return None
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
   
    @staticmethod
    def get_one(response: BaseResponse, idGet: int) -> VideoViewModel:
        try:
            document = categories.find_one({'id': idGet})
            if document is not None:
                obj = VideoViewModel(**document)
                response.message = f"Found item with id '{obj.id}'"
                return obj
            else:
                response.message = f"No item found for with _id '{idGet}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
           

    @staticmethod
    def get_many(response: BaseResponse, **kwargs):
        pass
        # try:
        #     keyIn = ""
        #     valueIn = ""

        #     for(key, value) in kwargs.items():
        #         keyIn = key
        #         valueIn = value

        #     if(keyIn == "" or valueIn == ""):
        #         response.message = "Invalid arguments."
        #         return None
            
        #     db_objects = db.query(VideoTable).filter_by(**kwargs).all()
        #     if db_objects is not None:
        #         response.message = f"Found items for {keyIn} with value '{valueIn}'"
        #         return [VideoViewModel.from_orm(obj) for obj in db_objects]
        #     else:
        #         response.message = f"No items found for {keyIn} with value '{valueIn}'"
        #         return None
            
        # except Exception as err:
        #     traceback.print_tb(err.__traceback__)
        #     response.error = str(err)
            

    @staticmethod
    def insert(response: BaseResponse, new_item: Video):
        try:
            if new_item is None:
                response.message = NULL_OBJ
                return None
            else:
                document = new_item.dict()
                document["_id"] = get_uuid()

                all_objects = VideoRepository.get_all(response)

                if all_objects is not None:
                    document["id"] = len(VideoRepository.get_all(response)) + 1
                else:
                    document["id"] = 1

                result = videos.insert_one(document)
                assert result.acknowledged
                return VideoRepository.get_one(response, document["id"])
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            

    @staticmethod
    def update(response: BaseResponse, new_obj):
        pass
        # try:
        #     if new_obj is None:
        #         response.message = NULL_OBJ
        #         return None
        #     else:
        #         old_obj = db.query(VideoTable).filter_by(id = new_obj.id).first()

        #         if old_obj is not None:
                    
        #             result = ""
        #             for key, value in new_obj.dict(exclude_unset = True).items():
        #                 if getattr(old_obj, key) != value:
        #                     # difference value
        #                     setattr(old_obj, key, value)
        #                     result += f"{key} has been updated to {value}, "

        #             response.message = result        
        #             db.commit()
        #             return VideoViewModel.from_orm(old_obj)
        #         else:
        #             response.message = f"No item found with id '{new_obj.id}'"
        #             return None

        # except Exception as err:
        #     traceback.print_tb(err.__traceback__)
        #     response.error = str(err)
        

    @staticmethod
    def updatePath(response: BaseResponse, id: int, new_path: str):
        pass
        # try:
        #     item = db.query(VideoTable).filter_by(id = id).first()

        #     if item is not None:  
        #         setattr(item, "path", new_path)
        #         db.commit()
        #         return VideoViewModel.from_orm(item)
        #     else:
        #         response.message = f"No item found with id '{id}'"
        #         return None

        # except Exception as err:
        #     traceback.print_tb(err.__traceback__)
        #     response.error = str(err)
           

    @staticmethod
    def updateAnnotation(response: BaseResponse, id: int, new_annotation: str):
        pass
        # try:
        #     item = db.query(VideoTable).filter_by(id = id).first()

        #     if item is not None:  
        #         setattr(item, "annotation", new_annotation)
        #         db.commit()
                
        #         return VideoViewModel.from_orm(item)
        #     else:
        #         response.message = f"No item found with id '{id}'"
        #         return None

        # except Exception as err:
        #     traceback.print_tb(err.__traceback__)
        #     response.error = str(err)
           
    @staticmethod
    def delete(response: BaseResponse, idDel: int):
        try:
            result = videos.delete_one({"id": idDel})
            if result.deleted_count == 1:
                response.message = f"Deleted item with id '{idDel}'"
            elif result.deleted_count == 0:
                response.message = f"No item found with id '{idDel}'"
            return result.deleted_count
        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)