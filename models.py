from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TransactionStatus(str,enum.Enum):
    PENDING="pending"
    SUCCESS="success"
    FAILED="failed"

class TransactionType(str,enum.Enum):
    CREDIT="credit"
    DEBIT="debit"
    TRANSFER="transfer"

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True,nullable=False)
    username=Column(String,unique=True,index=True,nullable=False)
    hashed_pass=Column(String,nullable=False)
    full_name=Column(String)
    is_active=Column(Integer,default=1)
    created_at=Column(DateTime,default=datetime.utcnow)
    
    api_key=Column(String,unique=True,index=True,nullable=True)
    
    wallet=relationship("Wallet",back_populates="owner",uselist=False)
    transactions=relationship("Transaction",back_populates="user",foreign_keys="Transaction.user_id")
    
    
class Wallet(Base):
    __tablename__="wallets"
    
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),unique=True)
    balance=Column(Float,default=0.0)
    currency=Column(String,default="INR")
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    owner=relationship("User",back_populates="wallet")
    
class Transaction(Base):
    __tablename__="transactions"
    
    id=Column(Integer,primary_key=True,index=True)
    transaction_id=Column(String,unique=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    
    amount=Column(Float,nullable=False)
    transaction_type=Column(SQLEnum(TransactionType),nullable=False)
    status=Column(SQLEnum(TransactionStatus),default=TransactionStatus.PENDING)
    
    from_user_id=Column(Integer,ForeignKey("users.id"),nullable=True)
    to_user_id=Column(Integer,ForeignKey("users.id"),nullable=True)
    
    description=Column(String,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    user=relationship("User",back_populates="transactions",foreign_keys=[user_id])
    