
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    