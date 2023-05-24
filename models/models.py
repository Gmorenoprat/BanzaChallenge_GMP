from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base, engine
import requests
from schemas.schemas import *

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    accounts = relationship("Account", back_populates="client")
    categories = relationship("Category", secondary="client_categories")


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="accounts")

    def get_total_usd(self):
        response = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        data = response.json()

        dolar_bolsa_rate = None
        for item in data:
            if item["casa"]["nombre"] == "Dolar Bolsa":
                dolar_bolsa_rate = float(item["casa"]["venta"].replace(",", "."))
                break

        if not dolar_bolsa_rate:
            raise Exception("Dolar Bolsa rate not found")

        balance_usd = self.balance / dolar_bolsa_rate

        return balance_usd


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    clients = relationship("Client", secondary="client_categories", back_populates="categories", overlaps="categories")


class ClientCategory(Base):
    __tablename__ = 'client_categories'

    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)


class Movement(Base):
    __tablename__ = 'movements'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Integer)
    date = Column(Date)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="movements")


Account.movements = relationship("Movement", order_by=Movement.id, back_populates="account")

# Bind the models to the Base and create the tables
Base.metadata.create_all(bind=engine)