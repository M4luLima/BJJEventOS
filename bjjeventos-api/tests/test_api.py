def test_root_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["sistema"] == "BJJEventOS API"

def test_cadastro_atleta_e_login(client):
    # 1. Cadastrar atleta
    user_payload = {
        "nome": "Marcus Buchecha",
        "email": "buchecha@bjj.com",
        "senha": "oss_password",
        "perfil": "atleta"
    }
    res = client.post("/api/v1/usuarios", json=user_payload)
    assert res.status_code == 201

    # 2. Login
    login_data = {"username": "buchecha@bjj.com", "password": "oss_password"}
    res_login = client.post("/api/v1/auth/login", data=login_data)
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()
