from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    username:str=Field(...,min_length=5,max_length=60)
    password:str=Field(...,min_length=8,max_length=60)
    fullname:Optional[str]=None
    
class UserLogin(BaseModel):
    username:str
    password:str
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    username:str
    full_name:Optional[str]=None
    is_active:bool
    created_at:datetime
    
    class Config:
        from_attributes=True
        
class Token(BaseModel):
    access_token:str
    token_type:str="bearer"

class WalletResponse(BaseModel):
    id:int
    user_id:int
    balance:float
    currency:str
    created_at:datetime
    updated_at:datetime
    
    class Config:
        from_attributes= True

class AddMoneyRequest(BaseModel):
    amount:float=Field(...,gt=0,description="Amount should be greater than Zero")
    description:Optional[str]="Add money to wallet"
class TransactionResponse(BaseModel):
    id:int
    transaction_id:str
    user_id:int
    amount:float
    transaction_type:str
    status:str
    from_user_id:Optional[int]
    to_user_id:Optional[int]
    description:Optional[str]
    created_at:datetime
    
    class Config:
        from_attributes=True
        
class TransferMoneyRequest(BaseModel):
    to_username:str=Field(...,min_length=6)
    amount:float=Field(...,gt=0,description="Amount must be greater than 0")
    description:Optional[str]="Money Transfer"
    