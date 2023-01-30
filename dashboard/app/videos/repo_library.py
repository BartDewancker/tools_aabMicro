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
                return list(map(lambda x: LibraryViewModel.from_orm(x), db_objects))
            else:
                response.message = f"No object of type {LibraryTable} were found in the database!"
                return None        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
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
            response.error = "Database error! Call the database administrator"
            db.rollback()


