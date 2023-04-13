from fastapi.testclient import TestClient

from .main import app
from .tests.resources import read_dataset_json

client = TestClient(app)
joke_id = 0
data = read_dataset_json()


def test_get_joke_not_found() -> None:
    response = client.get("/jokes/")

    assert response.status_code == 404
    assert response.json() == {"detail": "You have no jokes"}


def test_create_joke() -> None:
    joke_data = data["jokes"]["good_joke"]
    response = client.post("/jokes/", json=joke_data)

    global joke_id
    joke_id = response.json()["id"]

    assert response.status_code == 201
    assert response.json() == {"joke": joke_data["joke"], "id": joke_id}


def test_create_joke_existing() -> None:
    joke_data = data["jokes"]["good_joke"]
    response = client.post("/jokes/", json=joke_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Joke already exists"}


def test_create_joke_bad() -> None:
    joke_data = data["jokes"]["short_joke"]
    response = client.post("/jokes/", json=joke_data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Joke must be at least 5 characters long"}


def test_get_joke() -> None:
    joke_data = data["jokes"]["good_joke"]
    response = client.get("/jokes/")

    assert response.status_code == 200
    assert response.json() == {"joke": joke_data["joke"], "id": joke_id}


def test_get_joke_chuck() -> None:
    response = client.get("/jokes/?api=Chuck")
    assert response.status_code == 200


def test_get_joke_dad() -> None:
    response = client.get("/jokes/?api=Dad")
    assert response.status_code == 200


def test_get_joke_bad_() -> None:
    response = client.get("/jokes/?api=Goku")
    assert response.status_code == 400
    assert response.json() == {"detail": "You can only enter 'Chuck' or 'Dad'"}


def test_update_joke() -> None:
    joke_data = data["jokes"]["new_joke"]
    response = client.put(f"/jokes/{joke_id}", json=joke_data)

    assert response.status_code == 200
    assert response.json() == {"joke": joke_data["joke"], "id": joke_id}


def test_update_joke_existing() -> None:
    joke_data = data["jokes"]["new_joke"]
    response = client.put(f"/jokes/{joke_id}", json=joke_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Joke already exists"}


def test_update_joke_bad() -> None:
    joke_data = data["jokes"]["short_joke"]
    response = client.put(f"/jokes/{joke_id}", json=joke_data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Joke must be at least 5 characters long"}


def test_update_joke_not_found() -> None:
    joke_data = data["jokes"]["new_joke"]
    response = client.put("/jokes/999", json=joke_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Joke not found"}


def test_delete_joke() -> None:
    joke_data = data["jokes"]["new_joke"]
    response = client.delete(f"/jokes/{joke_id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Joke n°{joke_id} removed: {joke_data['joke']}"}


def test_delete_joke_not_found() -> None:
    response = client.delete("/jokes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Joke not found"}


def test_next_integer() -> None:
    params = data["math"]["next"]["params"]
    exp_response = data["math"]["next"]["response"]
    response = client.get(f"/math/next/{params}")

    assert response.status_code == 200
    assert response.json() == exp_response


def test_next_integera() -> None:
    params = data["math"]["lcm"]["params"]
    exp_response = data["math"]["lcm"]["response"]
    response = client.get(f"math/lcm/{params}")

    assert response.status_code == 200
    assert response.json() == exp_response
