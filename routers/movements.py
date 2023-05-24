from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Account, Movement
from schemas.schemas import *
from database import get_db

router = APIRouter()

# API Endpoints for Movements
@router.post("/movements", status_code=201)
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == movement.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if movement.type == MovementType.INCOME:
        account.balance += movement.amount
    elif movement.type == MovementType.EXPENSE:
        if account.balance < movement.amount:
            raise HTTPException(status_code=400, detail="Insufficient account balance")
        account.balance -= movement.amount

    new_movement = Movement(**movement.dict(), account=account)
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


@router.get("/movements/{movement_id}")
def get_movement(movement_id: int, db: Session = Depends(get_db)):
    movement = db.query(Movement).filter(Movement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")

    return movement


@router.delete("/movements/{movement_id}", status_code=204)
def delete_movement(movement_id: int, db: Session = Depends(get_db)):
    movement = db.query(Movement).filter(Movement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")

    # Access the associated account to revert transaction
    account = movement.account

    if movement.type == MovementType.INCOME:
        account.balance -= movement.amount
    elif movement.type == MovementType.EXPENSE:
        account.balance += movement.amount

    # Save the changes to the account
    db.add(account)
    db.commit()
    db.delete(movement)
    db.commit()
    return {"message": "Movement deleted successfully"}
