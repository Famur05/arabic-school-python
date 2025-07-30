from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError, JWTDecodeError
from app.routers import router
# import uvicorn
# import sys

# sys.path.insert(1, sys.path[0] + "/..")

app = FastAPI()


@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Not authenticated: missing access token."}
    )

@app.exception_handler(JWTDecodeError)
async def jwt_decode_error_handler(request: Request, exc: JWTDecodeError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or expired token."}
    )

app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", reload=True)
