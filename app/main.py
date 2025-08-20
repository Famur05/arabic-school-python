from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import register_exception_handlers
from app.routers import router

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

register_exception_handlers(app)

app.include_router(router)
