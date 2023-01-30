from database import db
from viewmodels import CategoryViewModel
from .schemas import CategoryTable
from .models import Category, BaseResponse, NULL_OBJ
import traceback

class CategoryRepository():
    
    @staticmethod
    def get_all(response: BaseResponse):
        try:
            db_objects = db.query(CategoryTable).all()
            if db_objects:
                #return [CategoryViewModel.from_orm(obj) for obj in db_objects]
                return list(map(lambda x: CategoryViewModel.from_orm(x), db_objects))
            else:
                response.message = f"No object of type {CategoryTable} were found in the database!"
                return None        
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            db.rollback()

    
    @staticmethod
    def get_one(response: BaseResponse, idGet: int):
        try:
            db_object = db.query(CategoryTable).filter_by(id = idGet).first()
            if db_object is not None:
                response.message = f"Found item with id '{db_object.id}'"
                return CategoryViewModel.from_orm(db_object)
            else:
                response.message = f"No item found for with id '{idGet}'"
                return None
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = "Database error! Call the database administrator"
            db.rollback()



