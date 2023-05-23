from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.models import *


# Database Connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

app = FastAPI()


# Database Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Endpoints
@app.post("/clients", status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(name=client.name, email=client.email)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get("/clients/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}")
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    existing_client = get_client(client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    existing_client.name = client.name
    existing_client.email = client.email
    db.commit()
    db.refresh(existing_client)
    return existing_client


@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    existing_client = get_client(client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(existing_client)
    db.commit()
    return {"message": "Client deleted successfully"}


@app.post("/accounts", status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    existing_client = get_client(account.client_id, db)
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    new_account = Account(name=account.name, balance=account.balance, client_id=account.client_id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@app.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.put("/accounts/{account_id}")
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    existing_account = get_account(account_id,db)
    if existing_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    existing_account.name = account.name
    existing_account.balance = account.balance
    db.commit()
    db.refresh(existing_account)
    return existing_account

@app.delete("/accounts/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()
    if existing_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(existing_account)
    db.commit()
    return {"message": "Account deleted successfully"}


# API Endpoints for Movements
@app.post("/movements", status_code=201)
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


@app.get("/movements/{movement_id}")
def get_movement(movement_id: int, db: Session = Depends(get_db)):
    movement = db.query(Movement).filter(Movement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")

    return movement


@app.delete("/movements/{movement_id}", status_code=204)
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

@app.post("/categories", status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(name=category.name)
    category = db.query(Category).filter(Category.name == new_category.name).first()
    if category:
        raise HTTPException(status_code=422 , detail="Category already created")
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@app.put("/categories/{category_id}")
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

@app.delete("/all")
def delete_all(db: Session = Depends(get_db)):
    db.query(Account).delete()
    db.query(Client).delete()
    db.query(Category).delete()
    db.query(ClientCategory).delete()
    db.query(Movement).delete()
    db.commit()
    return None


@app.post("/clients/{client_id}/categories", status_code=201)
def add_category_to_client(client_category_data: ClientCategoryCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_category_data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    category = db.query(Category).filter(Category.id == client_category_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    client_category = ClientCategory(client_id=client_category_data.client_id, category_id=client_category_data.category_id)
    db.add(client_category)
    db.commit()
    db.refresh(client_category)

    return client_category


@app.get("/clients/{client_id}/categories")
def get_client_categories(client_id: int, db: Session = Depends(get_db)):
    client = get_client(client_id, db)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    categories = db.query(Category).join(ClientCategory).filter(ClientCategory.client_id == client_id).all()

    return categories


@app.get("/categories/{category_id}/clients")
def get_categories_client(category_id: int, db: Session = Depends(get_db)):
    category = get_category(category_id, db)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    clients = db.query(Client).join(ClientCategory).filter(ClientCategory.category_id == category_id).all()

    return clients


@app.delete("/clients/{client_id}/categories/{category_id}", status_code=204)
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

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
