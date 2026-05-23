from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    gender: str
    phone: str
    email: str
    address: str
    created_at: datetime


class UserListResponse(BaseModel):
    items: list[UserRead]
    total: int
    limit: int
    offset: int 