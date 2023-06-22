from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str
    salary: int
    promotion: datetime

    class Config:
        orm_mode = True


class AuthModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
