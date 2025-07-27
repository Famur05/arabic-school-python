from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.user import Subscription
from models.user import LanguageLevel

class UserAddDTO(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserDTO(UserAddDTO):
    id: int

class UserInfoAddDTO(BaseModel):
    subscription: Subscription
    language_level: LanguageLevel
    user_id: int

class UserInfoDTO(UserInfoAddDTO):
    id: int         
    created_at: datetime
