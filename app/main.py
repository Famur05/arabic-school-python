from fastapi import FastAPI
from routers import user, root
import uvicorn

app = FastAPI()

app.include_router(root.router, tags=["Root"])
app.include_router(user.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
