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
            response.error = str(err)
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
            response.error = str(err)
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
            response.error = str(err)
            db.rollback()

    @staticmethod
    def insert(response: BaseResponse, new_item: Video):
        try:
            if new_item is None:
                response.message = NULL_OBJ
                return None
            else:
                db_object = VideoTable(**new_item.dict())
                db.add(db_object)
                db.commit()
                #db.refresh(db_object)
                response.message = "Item has been added successfully."
                return VideoViewModel.from_orm(db_object)
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    @staticmethod
    def update(response: BaseResponse, new_obj: Video):
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
    def updatePath(response: BaseResponse, id: int, new_path: str):
        try:
            item = db.query(VideoTable).filter_by(id = id).first()

            if item is not None:  
                setattr(item, "path", new_path)
                db.commit()
                return VideoViewModel.from_orm(item)
            else:
                response.message = f"No item found with id '{id}'"
                return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()


    @staticmethod
    def updateAnnotation(response: BaseResponse, id: int, new_annotation: str):
        try:
            item = db.query(VideoTable).filter_by(id = id).first()

            if item is not None:  
                setattr(item, "annotation", new_annotation)
                db.commit()
                
                return VideoViewModel.from_orm(item)
            else:
                response.message = f"No item found with id '{id}'"
                return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()


    @staticmethod
    def delete(response: BaseResponse, idDel: int):
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