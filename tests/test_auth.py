

def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "Ramiro Teste",
        "email": "tempmail@gmail.com",
        "password": "@SenhaDura123"
    })
    assert response.status_code == 201
    data = response.json()

    assert "user_id" in data
    assert data["message"] == "User registered successfully"

def test_register_duplicate_email(client):
    # Primeiro registro
    response1 = client.post("/auth/register", json={
        "name": "Ramiro Teste",
        "email": "tempmail1@gmail.com",
        "password": "@SenhaDura123"
    })
    assert response1.status_code == 201

    # Tentativa de registro com o mesmo email
    response2 = client.post("/auth/register", json={
        "name": "Outro User",
        "email": "tempmail1@gmail.com",
        "password": "@OutraSenha123"
    })
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"

def test_login_user(client):
    # Primeiro, registre um usuário para garantir que ele exista
    client.post("/auth/register", json={
        "name": "Ramiro Teste",
        "email": "tempmail2@gmail.com",
        "password": "@SenhaDura123"
    })

    response = client.post("/auth/login", json={
        "email": "tempmail2@gmail.com",
        "password": "@SenhaDura123"
    })
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid(client):
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "123456"
    })

    assert response.status_code == 400

def test_get_me(client):
    # cria usuário
    client.post("/auth/register", json={
        "name": "Ramiro",
        "email": "me@test.com",
        "password": "123456"
    })

    # login
    login = client.post("/auth/login", json={
        "email": "me@test.com",
        "password": "123456"
    })

    token = login.json()["access_token"]

    # acessar rota protegida
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@test.com"

