from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import Client, Category, CategoryCreate,CategoryUpdate, ClientCategory

router = APIRouter()


@router.post("/categories", status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(name=category.name)
    category = db.query(Category).filter(Category.name == new_category.name).first()
    if category:
        raise HTTPException(status_code=422, detail="Category already created")
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.put("/categories/{category_id}")
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}


@router.get("/categories/{category_id}/clients")
def get_categories_client(category_id: int, db: Session = Depends(get_db)):
    category = get_category(category_id, db)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    clients = db.query(Client).join(ClientCategory).filter(ClientCategory.category_id == category_id).all()

    return clients
