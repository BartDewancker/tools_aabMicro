from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from videos.router_video import router as router_video
from videos.router_category import router as router_category
from videos.router_library import router as router_library
from videos.graphql_video import Query as VideosQuery, Mutation as VideosMutation
from videos.graphql_category import Query as CategoriesQuery, Mutation as CategoriesMutation

# Import and start the database connection!
import database as db
db.start_db()

@strawberry.type
class Query(VideosQuery, CategoriesQuery):
    pass

@strawberry.type
class Mutation(VideosMutation, CategoriesMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(
    title="FastAPI for 'aad' project",
    description="'add' contains videos, categories, ...",
    version="0.0.1",
)

app.include_router(router_video, prefix="/videos")
app.include_router(router_category, prefix="/categories")
app.include_router(router_library, prefix="/libraries")
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    # Run the app with uvicorn and autoreload
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)