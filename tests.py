import time
import pytest
from fastapi.testclient import TestClient
from main import app
from models.models import Account
from schemas.schemas import *

clientTest = TestClient(app)


def pytest_namespace():
    return {
        'client': None,
        'account': None,
        'category': None,
        'clientcategory': None,
        'movement': None
    }


def test_create_client():
    client_data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    response = clientTest.post("/clients", json=client_data)
    assert response.status_code == 201
    client_result = response.json()
    assert "id" in client_result
    assert client_result["name"] == client_data["name"]
    assert client_result["email"] == client_data["email"]
    pytest.client = client_result


def test_get_client():
    client_id = pytest.client["id"]
    response = clientTest.get(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["id"] == client_id


def test_get_invalid_client():
    response = clientTest.get(f"/clients/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_update_client():
    client_id = pytest.client["id"]
    updated_data = {
        "id": client_id,
        "name": "Updated Name",
        "email": "updated.email@example.com"
    }
    response = clientTest.put(f"/clients/{client_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["email"] == updated_data["email"]


def test_delete_client():
    client_id = pytest.client["id"]
    response = clientTest.delete(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Client deleted successfully"


def test_get_erased_client():
    client_id = pytest.client["id"]
    response = clientTest.get(f"/clients/{client_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_create_account_erased_client():
    account_data = {
        "client_id": pytest.client["id"],
        "name": "Savings Account",
        "balance": 1000
    }
    response = clientTest.post("/accounts", json=account_data)
    assert response.status_code == 404


def test_create_client2():
    client_data = {
        "name": "Zoro",
        "email": "Roronoa@Zoro.com"
    }
    response = clientTest.post("/clients", json=client_data)
    assert response.status_code == 201
    client_result = response.json()
    assert "id" in client_result
    assert client_result["name"] == client_data["name"]
    assert client_result["email"] == client_data["email"]
    pytest.client = client_result


def test_create_account():
    account_data = {
        "client_id": pytest.client["id"],
        "name": "Savings Account",
        "balance": 10000
    }
    response = clientTest.post("/accounts", json=account_data)
    assert response.status_code == 201
    client_result = response.json()

    assert "id" in client_result
    assert client_result["name"] == account_data["name"]
    assert client_result["balance"] == account_data["balance"]
    assert client_result["client_id"] == account_data["client_id"]
    pytest.account = client_result


def test_get_account():
    account_id = pytest.account["id"]
    response = clientTest.get(f"/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["id"] == account_id
    assert response.json()["name"] == pytest.account["name"]


def test_update_account():
    updated_account_data = {
        "id": pytest.account['id'],
        "name": "Updated Account",
        "balance": 2000.0
    }
    response = clientTest.put(f"/accounts/{pytest.account['id']}", json=updated_account_data)
    assert response.status_code == 200
    updated_account = response.json()
    assert updated_account["id"] == pytest.account['id']
    assert updated_account["name"] == updated_account_data["name"]
    assert updated_account["balance"] == updated_account_data["balance"]


def test_delete_account():
    response = clientTest.delete(f"/accounts/{pytest.account['id']}")
    assert response.status_code == 204


def test_get_deleted_account():
    account_id = pytest.account["id"]
    response = clientTest.get(f"/accounts/{account_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"


def test_update_deleted_account():
    updated_account_data = {
        "id": pytest.account['id'],
        "name": "Updated Account",
        "balance": 2000.0
    }
    response = clientTest.put(f"/accounts/{pytest.account['id']}", json=updated_account_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"


def test_create_category(name="Category1"):
    category_data = {
        "name": str(pytest.account["id"]) + name
    }
    response = clientTest.post("/categories", json=category_data)
    pytest.category = response.json()
    assert response.status_code == 201
    assert response.json()["name"] == category_data["name"]


def test_create_category_already_created():
    category_data = {
        "name": pytest.category["name"]
    }
    response = clientTest.post("/categories", json=category_data)
    assert response.status_code == 422


def test_get_categories():
    response = clientTest.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.status_code == 200


def test_get_category():
    category_id = pytest.category["id"]
    response = clientTest.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["id"] == category_id


def test_update_category():
    category_id = pytest.category["id"]
    updated_data = {
        "id": category_id,
        "name": "Updated Name",
    }
    response = clientTest.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]


def test_delete_category():
    category_id = pytest.category["id"]
    response = clientTest.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted"

def test_get_deleted_category():
    category_id = pytest.category["id"]
    response = clientTest.get(f"/categories/{category_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_update_deleted_category():
    category_id = pytest.category["id"]
    updated_data = {
        "id": category_id,
        "name": "Updated Name",
    }
    response = clientTest.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_create_category2(name="Category2"):
    category_data = {
        "name": str(pytest.account["id"]) + name
    }
    response = clientTest.post("/categories", json=category_data)
    pytest.category = response.json()
    assert response.status_code == 201
    assert response.json()["name"] == category_data["name"]




def test_create_category3(name="Category3"):
    category_data = {
        "name": str(pytest.account["id"]) + name
    }
    response = clientTest.post("/categories", json=category_data)
    pytest.category = response.json()
    assert response.status_code == 201
    assert response.json()["name"] == category_data["name"]


def test_add_category_to_client():
    client_category_data = {
        "client_id": pytest.client["id"],
        "category_id": pytest.category["id"]
    }
    response = clientTest.post(f"/clients/{pytest.client['id']}/categories", json=client_category_data)

    assert response.status_code == 201
    assert response.json()["client_id"] == client_category_data["client_id"]
    assert response.json()["category_id"] == client_category_data["category_id"]

    pytest.clientcategory = response.json()


def test_get_client_categories():
    response = clientTest.get(f"/clients/{pytest.clientcategory['client_id']}/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) >= 1


def test_get_categories_client():
    response = clientTest.get(f"/categories/{pytest.clientcategory['category_id']}/clients")
    assert response.status_code == 200
    clients = response.json()
    assert len(clients) >= 1


def test_get_client_categories_invalid_client():
    response = clientTest.get(f"/clients/{-1}/categories")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_get_categories_client_invalid_client():
    response = clientTest.get(f"/categories/{-1}/clients")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_remove_category_from_client():
    response = clientTest.delete(
        f"/clients/{pytest.clientcategory['client_id']}/categories/{pytest.clientcategory['category_id']}")
    assert response.status_code == 204

    response = clientTest.get(f"/clients/{pytest.clientcategory['client_id']}/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 0


def test_remove_category_from_invalid_client():
    response = clientTest.delete(f"/clients/{-1}/categories/{pytest.clientcategory['category_id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_remove_invalid_category_from_client():
    response = clientTest.delete(f"/clients/{pytest.clientcategory['client_id']}/categories/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_remove_not_associated_category_from_client():
    response = clientTest.delete(
        f"/clients/{pytest.clientcategory['client_id']}/categories/{pytest.clientcategory['category_id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category is not associated with the client"


def test_create_account2():
    account_data = {
        "client_id": pytest.client["id"],
        "name": "Savings Account",
        "balance": 0
    }
    response = clientTest.post("/accounts", json=account_data)
    assert response.status_code == 201
    client_result = response.json()

    assert "id" in client_result
    assert client_result["name"] == account_data["name"]
    assert client_result["balance"] == account_data["balance"]
    assert client_result["client_id"] == account_data["client_id"]
    pytest.account = client_result


def test_create_movement_income():
    movement_data = {
        "type": MovementType.INCOME,
        "amount": 100,
        "date": "2023-05-20",
        "account_id": pytest.account["id"]
    }

    response = clientTest.post("/movements", json=movement_data)
    assert response.status_code == 201

    pytest.movement = response.json()


def test_get_movement():
    response = clientTest.get(f"/movements/{pytest.movement['id']}")
    assert response.status_code == 200
    assert response.json()["type"] == "income"
    assert response.json()["amount"] == 100
    assert response.json()["date"] == "2023-05-20"
    assert response.json()["account_id"] == pytest.movement['account_id']


def test_delete_movement():
    response = clientTest.delete(f"/movements/{pytest.movement['id']}")
    assert response.status_code == 204


def test_get_movement_not_found():
    response = clientTest.get(f"/movements/{pytest.movement['id']}")
    assert response.status_code == 404


def test_create_movement_income2():
    movement_data = {
        "type": MovementType.INCOME,
        "amount": 99,
        "date": "2023-05-20",
        "account_id": pytest.account["id"]
    }

    response = clientTest.post("/movements", json=movement_data)
    assert response.status_code == 201

    pytest.movement = response.json()


def test_create_movement_expense():
    movement_data = {
        "type": MovementType.EXPENSE,
        "amount": 100,
        "date": "2023-05-20",
        "account_id": pytest.account["id"]
    }

    response = clientTest.post("/movements", json=movement_data)
    assert response.status_code == 201

    pytest.movement = response.json()


def test_create_movement_expense():
    movement_data = {
        "type": MovementType.EXPENSE,
        "amount": 1,
        "date": "2023-05-20",
        "account_id": pytest.account["id"]
    }

    response = clientTest.post("/movements", json=movement_data)
    assert response.status_code == 201

    pytest.movement = response.json()


def test_create_movement_expense_no_balance():
    movement_data = {
        "type": MovementType.EXPENSE,
        "amount": 1000,
        "date": "2023-05-20",
        "account_id": pytest.account["id"]
    }

    response = clientTest.post("/movements", json=movement_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient account balance"
    pytest.movement = response.json()


def test_balance_uds():
    account = Account()
    account.balance = 1000
    uds = account.get_total_usd()
    assert uds < account.balance

# Run the tests
# def run_tests():
#
#     test_create_client()
#     test_get_client()
#     test_update_client()
#     test_delete_client()
#     test_create_account_erasedClient()
#     test_create_client()
#     test_create_account()
#     test_get_account()
#     test_update_account()
#     test_delete_account()
#     test_create_account2()
#     test_create_category()
#     test_create_category_alreadyCreated()
#     test_get_categories()
#     test_get_category()
#     test_update_category()
#     test_delete_category()
#     test_create_category2()
#     test_add_category_to_client()
#     test_create_category3()
#     test_add_category_to_client()
#     test_get_client_categories()
#     test_create_client()
#     test_add_category_to_client()
#     test_get_categories_client()
#     test_get_client_categories_invalid_client()
#     test_get_categories_client_invalid_client()
#     test_remove_category_from_client()
#     test_remove_category_from_invalid_client()
#     test_remove_invalid_category_from_client()
#     test_remove_not_associated_category_from_client()
#     test_create_movement_income()
#     test_get_movement()
#     test_delete_movement()
#     test_get_movement_not_found()
#     test_create_movement_expense()
#     test_create_movement_expense_no_balance()
#     test_balance_uds()

##run_tests()


# reset db
# def deletealltest():
#     response = clientTest.delete(f"/resetBase")
#     assert response.status_code == 200
# def delete_all():
#     deletealltest()
# delete_all()
