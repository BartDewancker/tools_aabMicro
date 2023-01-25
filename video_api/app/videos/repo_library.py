from database import db
from viewmodels import LibraryViewModel
from .schemas import LibraryTable
from .models import Library, BaseResponse, NULL_OBJ
import traceback

class LibraryRepository():
    
    @staticmethod
    def get_all(response: BaseResponse):
        try:
            db_objects = db.query(LibraryTable).all()
            if db_objects:
                return list(map(lambda x: Library.from_orm(x), db_objects))
            else:
                response.message = f"No object of type {LibraryTable} were found in the database!"
                return None        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    
    @staticmethod
    def get_one(response: BaseResponse, idGet: int):
        try:
            db_object = db.query(LibraryTable).filter_by(id = idGet).first()
            if db_object is not None:
                response.message = f"Found item with id '{db_object.id}'"
                return LibraryViewModel.from_orm(db_object)
            else:
                response.message = f"No item found for with id '{idGet}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()


    @staticmethod
    def insert(response: BaseResponse, new_item: Library):
        try:
            if new_item is None:
                response.message = NULL_OBJ
                return None
            else:
                db_object = LibraryTable(**new_item.dict())
                db.add(db_object)
                db.commit()
                db.refresh(db_object)
                response.message = "Item has been added successfully."
                return LibraryViewModel.from_orm(db_object)
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()
    

    @staticmethod
    def update(response: BaseResponse, new_obj: Library):
        try:
            if new_obj is None:
                response.message = NULL_OBJ
                return None
            else:
                old_obj = db.query(LibraryTable).filter_by(id = new_obj.id).first()

                if old_obj is not None:
                    
                    result = ""
                    for key, value in new_obj.dict(exclude_unset = True).items():
                        if getattr(old_obj, key) != value:
                            # difference value
                            setattr(old_obj, key, value)
                            result += f"{key} has been updated to {value}, "

                    response.message = result        
                    db.commit()
                    
                    return LibraryViewModel.from_orm(old_obj)
                else:
                    response.message = f"No item found with id '{new_obj.id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()

    @staticmethod
    def delete(response: BaseResponse, idDel: int):
        try:
            num_rows_deleted = db.query(LibraryTable).filter_by(id = idDel).delete()
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

