from databaseNew import db
from viewmodels import VideoViewModel

from .schemas import VideoTable
from .models import VideoResponse, NULL_OBJ
import traceback

class VideoRepository():
    
    def get_all(response: VideoResponse):
        try:
            db_objects = db.query(VideoTable).all()
            if db_objects:
                return list(map(lambda x: VideoViewModel.from_orm(x), db_objects))
            else:
                response.message = f"No object of type {VideoTable} were found in the database!"
                return None
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    def get_one(idGet: int, response: VideoResponse):
        try:
            db_object = db.query(VideoTable).filter_by(id = idGet).first()
            if db_object is not None:
                response.message = f"Found item with id '{idGet}'"
                return VideoViewModel.from_orm(db_object)
            else:
                response.message = f"No item found with id '{idGet}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    @staticmethod
    def insert(new_video: VideoTable, response: VideoResponse):
        try:
            if new_video is None:
                response.message = NULL_OBJ
                return None
            else:
                db_object = VideoTable(**new_video.dict())
                db.add(db_object)
                db.commit()
                db.refresh(db_object)
                response.message = "Item has been added successfully."
                return db_object
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    @staticmethod
    def update(new_obj, response: VideoResponse):
        try:
            if new_obj is None:
                response.message = NULL_OBJ
                return None
            else:
                old_obj = db.query(VideoTable).filter_by(id = new_obj.id).first()

                if old_obj is not None:
                    
                    result = ""
                    for key, value in new_obj.dict(exclude_unset = True).items():
                        if getattr(old_obj, key) != value:
                            # difference value
                            setattr(old_obj, key, value)
                            result += f"{key} has been updated to {value}, "

                    response.message = result        
                    db.commit()
                    
                    return VideoViewModel.from_orm(old_obj)
                else:
                    response.message = f"No item found with id '{new_obj.id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    @staticmethod
    def delete(idDel: int, response: VideoResponse):
        try:
            num_rows_deleted = db.query(VideoTable).filter_by(id = idDel).delete()
            if num_rows_deleted == 1:
                response.message = f"Deleted item with id '{idDel}'"
            elif num_rows_deleted == 0:
                response.message = f"No item found with id '{idDel}'"
            db.commit()
            return num_rows_deleted
        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()