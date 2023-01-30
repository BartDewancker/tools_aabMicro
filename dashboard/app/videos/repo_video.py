from database import db
from viewmodels import VideoViewModel
from .schemas import VideoTable
from .models import Video, BaseResponse, NULL_OBJ
import traceback

class VideoRepository():
    
    @staticmethod
    def get_all(response: BaseResponse):
        try:
            db_objects = db.query(VideoTable).all()
            if db_objects:
                return list(map(lambda x: VideoViewModel.from_orm(x), db_objects))
            else:
                response.message = f"No object of type {VideoTable} were found in the database!"
                return None
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            db.rollback()

    @staticmethod
    def get_one(response: BaseResponse, **kwargs):
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
            
            db_object = db.query(VideoTable).filter_by(**kwargs).first()
            if db_object is not None:
                response.message = f"Found item with id '{db_object.id}'"
                return VideoViewModel.from_orm(db_object)
            else:
                response.message = f"No item found for {keyIn} with value '{valueIn}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            db.rollback()

    @staticmethod
    def get_many(response: BaseResponse, **kwargs):
        try:
            keyIn = ""
            valueIn = ""

            for(key, value) in kwargs.items():
                keyIn = key
                valueIn = value

            if(keyIn == "" or valueIn == ""):
                response.message = "Invalid arguments."
                return None
            
            db_objects = db.query(VideoTable).filter_by(**kwargs).all()
            if db_objects is not None:
                response.message = f"Found items for {keyIn} with value '{valueIn}'"
                return [VideoViewModel.from_orm(obj) for obj in db_objects]
            else:
                response.message = f"No items found for {keyIn} with value '{valueIn}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            db.rollback()
