from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: Optional[str]
    website: Optional[str]
