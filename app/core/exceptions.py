from fastapi import Request
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError, JWTDecodeError

def register_exception_handlers(app):
    @app.exception_handler(MissingTokenError)
    async def missing_token_handler(request: Request, exc: MissingTokenError):
        return JSONResponse(
            status_code=401, content={"detail": "Not authenticated: missing access token."}
        )

    @app.exception_handler(JWTDecodeError)
    async def jwt_decode_error_handler(request: Request, exc: JWTDecodeError):
        return JSONResponse(
            status_code=401, content={"detail": "Invalid or expired token."}
        )
