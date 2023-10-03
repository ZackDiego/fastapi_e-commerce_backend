from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# pydantic schema
class ProductBase(BaseModel):
    product_name: str
    cost_price: float
    quantity: Optional[int] = 0

class Create_Product(ProductBase):
    pass

class Update_Product(ProductBase):
    pass




class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Product(ProductBase):
    product_id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class Response_Product(BaseModel):
    Product: Product
    rating_num: int
    avg_rating: Optional[float] = 0
    class Config:
        orm_mode = True

## Rating
class Create_Rating(BaseModel):
    rating: int
    product_id: int
    message: Optional[str] = ""
    
    
class Response_Rating(Create_Rating):
    rater_id: int