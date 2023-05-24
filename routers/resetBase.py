# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from models.models import Account, Movement, Client, Category, ClientCategory
# from schemas.schemas import *
# from database import get_db
#
# router = APIRouter()
#
# @router.delete("/resetBase")
# def delete_all(db: Session = Depends(get_db)):
#     db.query(Account).delete()
#     db.query(Client).delete()
#     db.query(Category).delete()
#     db.query(ClientCategory).delete()
#     db.query(Movement).delete()
#     db.commit()
#     return None
