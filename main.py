from fastapi import FastAPI
from routers import accounts, categories, clients, movements

# ,resetBase

app = FastAPI()

app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(clients.router)
app.include_router(movements.router)

# OnlyForTestDontUseInProduction
# app.include_router(resetBase.router)
