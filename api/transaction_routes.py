from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app import models,schemas,auth

router=APIRouter(prefix="/transaction",tags=["Transactions"])

@router.post("/transfer",response_model=schemas.TransactionResponse)
async def transfer_money(
    request:schemas.TransferMoneyRequest,
    current_user:models.User=Depends(auth.get_current_user),
    db:Session=Depends(get_db)
):
    if request.to_username==current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Cannot transfer to yourself"
        )
    
    recipient=db.query(models.User).filter(
        models.User.username==request.to_username
    ).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )
        
    sender_wallet=db.query(models.Wallet).filter(
        models.Wallet.user_id==current_user.id
    ).first()
    recipient_wallet=db.query(models.Wallet).filter(models.Wallet.user_id==recipient.id).first()
    if sender_wallet.balance<request.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Insufficient Balance")
    
    transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}"
    sender_transaction=models.Transaction(
        transaction_id=transaction_id,
        user_id=current_user.id,
        amount=request.amount,
        transaction_type=models.TransactionType.TRANSFER,
        status=models.TransactionStatus.SUCCESS,
        from_user_id=current_user.id,
        to_user_id=recipient.id,
        description=f"Sent to {recipient.username}"
    )
    
    recipient_transaction=models.Transaction(
        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
        user_id=recipient.id,
        amount=request.amount,
        transaction_type=models.TransactionType.TRANSFER,
        status=models.TransactionStatus.SUCCESS,
        from_user_id=current_user.id,
        to_user_id=recipient.id,
        description=f"Received From{current_user.username}"
    )
    sender_wallet.balance-=request.amount
    sender_wallet.updated_at=datetime.utcnow()
    
    recipient_wallet.balance+=request.amount
    recipient_wallet.updated_at=datetime.utcnow()
    
    db.add(sender_transaction)
    db.add(recipient_transaction)
    db.commit()
    db.refresh(sender_transaction)
    return sender_transaction
@router.get("/history",response_model=List[schemas.TransactionResponse])
async def get_transaction_history(limit:int=Query(default=10,ge=1,le=100),
current_user:models.User=Depends(auth.get_current_user),db:Session=Depends(get_db)):
    transactions=db.query(models.Transaction).filter(models.Transaction.user_id==current_user.id).order_by(
        models.Transaction.created_at.desc()
    ).limit(limit).all()
    
    return transactions