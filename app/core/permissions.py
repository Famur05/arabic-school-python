from fastapi import Depends, HTTPException
from authx.schema import TokenPayload
from app.config.auth import auth


def admin_required(
    payload: TokenPayload = Depends(auth.access_token_required),
) -> TokenPayload:
    role = payload.role
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload


def user_required(
    payload: TokenPayload = Depends(auth.access_token_required),
) -> TokenPayload:
    role = payload.role
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="User access required")
    return payload
