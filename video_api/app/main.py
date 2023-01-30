from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from videos.router_video import router as router_video
from videos.router_video import router2 as router_video2
from videos.router_category import router as router_category
from videos.router_library import router as router_library
from videos.graphql_video import Query as VideoQuery, Mutation as VideoMutation
from videos.graphql_category import Query as CategoryQuery, Mutation as CategoryMutation
from videos.graphql_library import Query as LibraryQuery, Mutation as LibraryMutation

# Import and start the database connection!
import database as db
db.start_db()

@strawberry.type
class Query(VideoQuery, CategoryQuery, LibraryQuery):
    pass

@strawberry.type
class Mutation(VideoMutation, CategoryMutation, LibraryMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(
    title="API for 'Araani Analytics Benchmarking' project",
    description="Contains videos metadata and annotations",
    version="1.0.0",
)

app.include_router(router_video, prefix="/videos_1")
app.include_router(router_video2, prefix="/videos_2")
app.include_router(router_category, prefix="/categories")
app.include_router(router_library, prefix="/libraries")
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    # Run the app with uvicorn and autoreload
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)