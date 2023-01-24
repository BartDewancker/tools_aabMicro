from typing import Optional, List, Union
import strawberry

from .repo_library import LibraryRepository
from .models import Library, BaseResponse, NULL_OBJ
from graphql_models import LibraryInput, LibraryType, ListOfCategories, BaseMessage, LibraryReturn

repo = LibraryRepository

@strawberry.type
class Query:
      
    @strawberry.field
    def library_get_all(self) -> Union[ListOfCategories, BaseMessage]:
      
        res = BaseResponse(message="", error="")
        items: List[LibraryType] = repo.get_all(res)
        
        if res.error != "":
            return BaseMessage(message = res.error)
        elif (items is not None and len(items) > 0):
            return ListOfCategories(videos=items)
        else:
            return BaseMessage(message = res.message)
    
    @strawberry.field
    def library_get_one(self, id: int = strawberry.UNSET) -> LibraryReturn:
        res = BaseResponse(message="", error="")

        if (id is not strawberry.UNSET):
            item = repo.get_one(res, id)
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
    def library_insert(self, item: LibraryInput) -> LibraryReturn:
   
        res = BaseResponse(message="", error="")
        added_item = repo.insert(res, Library(**item.__dict__))

        if res.error != "":
            return BaseMessage(message = res.error)
        elif(res.message == NULL_OBJ):
            return BaseMessage(message = res.message)
        elif (added_item is not None):
            return added_item
        
    @strawberry.mutation
    def library_update(self, item: LibraryInput) -> LibraryReturn:
   
        res = BaseResponse(message="", error="")
        updated_item = repo.update(res, Library(**item.__dict__))

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
    def library_delete(self, id: int = strawberry.UNSET) -> str:
   
        res = BaseResponse(message="", error="")
        num_rows_deleted = repo.delete(res, id)

        if res.error != "":
            return res.error
        elif (num_rows_deleted > 0):
            return res.message
        else:
            return res.message
        
        
        
       