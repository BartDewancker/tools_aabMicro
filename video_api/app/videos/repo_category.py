from database import db
from viewmodels import CategoryViewModel
from .schemas import CategoryTable
from .models import CategoryResponse, NULL_OBJ
import traceback

class CategoryRepository():
    
    @staticmethod
    def get_all(response: CategoryResponse):

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
            response.error = str(err)
            db.rollback()
    
    @staticmethod
    def update(response: CategoryResponse, new_obj):
        try:
            if new_obj is None:
                response.message = NULL_OBJ
                return None
            else:
                old_obj = db.query(CategoryTable).filter_by(id = new_obj.id).first()

                if old_obj is not None:
                    
                    result = ""
                    for key, value in new_obj.dict(exclude_unset = True).items():
                        if getattr(old_obj, key) != value:
                            # difference value
                            setattr(old_obj, key, value)
                            result += f"{key} has been updated to {value}, "

                    response.message = result        
                    db.commit()
                    
                    return CategoryViewModel.from_orm(old_obj)
                else:
                    response.message = f"No item found with id '{new_obj.id}'"
                    return None

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            response.error = str(err)
            db.rollback()