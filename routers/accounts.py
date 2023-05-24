from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Account
from routers.clients import get_client
from schemas.schemas import *
from database import get_db

router = APIRouter()

@router.post("/accounts", status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    existing_client = get_client(account.client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    new_account = Account(name=account.name, balance=account.balance, client_id=account.client_id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/accounts/{account_id}")
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    existing_account = get_account(account_id,db)
    if existing_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    existing_account.name = account.name
    existing_account.balance = account.balance
    db.commit()
    db.refresh(existing_account)
    return existing_account

@router.delete("/accounts/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()
    if existing_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(existing_account)
    db.commit()
    return {"message": "Account deleted successfully"}

