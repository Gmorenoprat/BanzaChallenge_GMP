from datetime import date
from pydantic import BaseModel
from sqlalchemy import Enum


# Pydantic Models
class ClientBase(BaseModel):
    name: str
    email: str
class ClientCreate(ClientBase):
    pass
class ClientUpdate(ClientBase):
    id: int

class AccountBase(BaseModel):
    name: str
    balance: int
class AccountCreate(AccountBase):
    client_id: int
class AccountUpdate(AccountBase):
    id: int
class AccountResponse(AccountBase):
    id: int
    client_id: int



class MovementType(str,Enum):
    INCOME = "income"
    EXPENSE = "expense"

class MovementBase(BaseModel):
    amount: int
    date: date

class MovementCreate(MovementBase):
    type: MovementType
    account_id: int

class MovementUpdate(MovementBase):
    id: int
class MovementResponse(MovementBase):
    id: int
    client_id: int
class CategoryBase(BaseModel):
    name: str
class CategoryCreate(CategoryBase):
    pass
class CategoryUpdate(CategoryBase):
    id: int
class CategoryResponse(CategoryBase):
    id: int


class ClientCategoryBase(BaseModel):
    client_id: int
    category_id: int


class ClientCategoryCreate(ClientCategoryBase):
    pass


class ClientCategory(ClientCategoryBase):
    class Config:
        orm_mode = True