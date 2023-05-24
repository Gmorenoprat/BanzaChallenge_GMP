from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.models import Client, Category, ClientCategory
from routers.categories import get_category
from schemas.schemas import ClientCreate, ClientUpdate, ClientCategoryCreate

router = APIRouter()


@router.post("/clients", status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(name=client.name, email=client.email)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/clients/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/clients/{client_id}")
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    existing_client = get_client(client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    existing_client.name = client.name
    existing_client.email = client.email
    db.commit()
    db.refresh(existing_client)
    return existing_client


@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    existing_client = get_client(client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(existing_client)
    db.commit()
    return {"message": "Client deleted successfully"}


@router.post("/clients/{client_id}/categories", status_code=201)
def add_category_to_client(client_category_data: ClientCategoryCreate, db: Session = Depends(get_db)):
    client = get_client(client_category_data.client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    category = get_category(client_category_data.category_id, db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    client_category = ClientCategory(client_id=client_category_data.client_id,
                                     category_id=client_category_data.category_id)
    db.add(client_category)
    db.commit()
    db.refresh(client_category)

    return client_category


@router.get("/clients/{client_id}/categories")
def get_client_categories(client_id: int, db: Session = Depends(get_db)):
    client = get_client(client_id, db)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    categories = db.query(Category).join(ClientCategory).filter(ClientCategory.client_id == client_id).all()

    return categories


@router.delete("/clients/{client_id}/categories/{category_id}", status_code=204)
def remove_category_from_client(client_id: int, category_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    client_category = (
        db.query(ClientCategory)
        .filter(ClientCategory.client_id == client.id, ClientCategory.category_id == category.id)
        .first()
    )
    if not client_category:
        raise HTTPException(status_code=404, detail="Category is not associated with the client")

    db.delete(client_category)
    db.commit()

    return {"message": "Category removed from client successfully"}
