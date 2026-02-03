from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.database import get_db
from app import models,schemas,auth

router=APIRouter(prefix="/wallet",tags=["Wallet"])

@router.get("/balance",response_model=schemas.WalletResponse)
async def get_wallet_balance(
    current_user:models.User=Depends(auth.get_current_user),
    db:Session=Depends(get_db)
):
    wallet=db.query(models.Wallet).filter(models.Wallet.user_id==current_user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Wallet not found"
        )
    return wallet
@router.post("/add-Money",response_model=schemas.TransactionResponse)
async def add_money(
    request:schemas.AddMoneyRequest,
    current_user:models.User=Depends(auth.get_current_user),
    db:Session=Depends(get_db)
):
    wallet=db.query(models.Wallet).filter(models.Wallet.user_id==current_user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Wallet not found "
        )
        
    transaction=models.Transaction(
        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
        user_id=current_user.id,
        amount=request.amount,
        transaction_type=models.TransactionType.CREDIT,
        status=models.TransactionStatus.SUCCESS,
        description=request.description
    )
    
    wallet.balance+=request.amount
    wallet.updated_at=datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction
@router.get("/",response_model=schemas.WalletResponse)
async def get_wallet(
    current_user:models.User=Depends(auth.get_current_user),
    db:Session=Depends(get_db)
):
    wallet=db.query(models.Wallet).filter(models.Wallet.user_id==current_user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Wallet not found"
        )
    return wallet