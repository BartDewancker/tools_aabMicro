from typing import Optional, List, Union
import strawberry

from .repo_category import CategoryRepository
from .models import Category, BaseResponse, NULL_OBJ
from graphql_models import CategoryInput, CategoryType, CategoryViewModelType, ListOfCategories, BaseMessage, CategoryReturn

@strawberry.type
class Query:
      
    @strawberry.field
    def category_get_all(self) -> Union[ListOfCategories, BaseMessage]:
      
        res = BaseResponse(message="", error="")
        items: List[CategoryType] = CategoryRepository.get_all(res)
        
        if res.error != "":
            return BaseMessage(message = res.error)
        elif (items is not None and len(items) > 0):
            return ListOfCategories(videos=items)
        else:
            return BaseMessage(message = res.message)
    
    @strawberry.field
    def category_get_one(self, id: int = strawberry.UNSET) -> CategoryReturn:
        res = BaseResponse(message="", error="")

        if (id is not strawberry.UNSET):
            item = CategoryRepository.get_one(res, id)
            if res.error != "":
                return BaseMessage(message = res.error)
            elif (item is not None):
                print(res.message)
                return item
            else:
                return BaseMessage(message = res.message)
            
@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def category_insert(self, item: CategoryInput) -> CategoryReturn:
   
        res = BaseResponse(message="", error="")
        added_item = CategoryRepository.insert(res, Category(**item.__dict__))

        if res.error != "":
            return BaseMessage(message = res.error)
        elif(res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (added_item is not None):
            return added_item
        
    @strawberry.mutation
    def category_update(self, item: CategoryInput) -> CategoryReturn:
   
        res = BaseResponse(message="", error="")
        updated_item = CategoryRepository.update(res, Category(**item.__dict__))

        if res.error != "":
            return  BaseMessage(message = res.error)
        elif (res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (updated_item is not None):
            print(res.message)
            return updated_item
        else:
            return BaseMessage(message = res.message)
        
    
    @strawberry.mutation
    def category_delete(self, id: int = strawberry.UNSET) -> str:
   
        res = BaseResponse(message="", error="")
        num_rows_deleted = CategoryRepository.delete(res, id)

        if res.error != "":
            return res.error
        elif (num_rows_deleted > 0):
            return res.message
        else:
            return res.message
        
        
        
       