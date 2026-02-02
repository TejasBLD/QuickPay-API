from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import or_
from app.database import get_db
from app import models,schemas,auth
from app.config import settings


router= APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/register",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user_data:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(
    or_(
        models.User.email == user_data.email,
        models.User.username == user_data.username
    )
).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email or username already registered")
    
    hashed_password=auth.get_hashed_password(user_data.password)
    
    New_user=models.User(
        email=user_data.email,
        username=user_data.username,
        hashed_pass=hashed_password,
        full_name=user_data.fullname
        
    )
    db.add(New_user)
    db.commit()
    db.refresh(New_user)
    
    wallet=models.Wallet(user_id=New_user.id)
    db.add(wallet)
    db.commit()
    return New_user
@router.post("/login",response_model=schemas.Token)
async def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    user=auth.authenticate_user(db,form_data.username,form_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect credentials",headers={"WWW-Authenticate":"Bearer"})
    
    access_token_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=auth.create_access_token(
        data={"sub":user.username},
        expires_delta=access_token_expires
    )
    return{
        "access_token":access_token,"token_type":"bearer"
    }
@router.get("/me",response_model=schemas.UserResponse)
async def get_current_user_info(current_user:models.User=Depends(auth.get_current_user)):
    return current_user