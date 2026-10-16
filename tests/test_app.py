def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_db_ping(client):
    response = client.get("/db/ping")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["dialect"] == "sqlite"


def test_items_vacio(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}


def test_crear_y_listar_item(client):
    response = client.post("/items", params={"nombre": "test item"})
    assert response.status_code == 201
    creado = response.json()
    assert creado["nombre"] == "test item"
    assert creado["id"] == 1

    response = client.get("/items")
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["nombre"] == "test item"
