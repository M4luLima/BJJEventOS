from datetime import datetime, timedelta, date

def test_01_root_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["sistema"] == "BJJEventOS API"

def test_02_cadastro_usuario_e_hash(client):
    payload = {
        "nome": "Marcus Buchecha",
        "email": "buchecha@bjj.com",
        "senha": "senhaSegura123",
        "perfil": "atleta"
    }
    response = client.post("/api/v1/usuarios", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "buchecha@bjj.com"
    assert "senha" not in data

def test_03_login_e_token_jwt(client):
    client.post("/api/v1/usuarios", json={
        "nome": "Organizador CBJJ",
        "email": "org@cbjj.com",
        "senha": "orgPassword123",
        "perfil": "organizador"
    })
    
    login_resp = client.post("/api/v1/auth/login", data={
        "username": "org@cbjj.com",
        "password": "orgPassword123"
    })
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["perfil"] == "organizador"

def test_04_rn01_email_duplicado(client):
    user_data = {
        "nome": "Admin Principal",
        "email": "admin@bjj.com",
        "senha": "adminPassword123",
        "perfil": "admin"
    }
    client.post("/api/v1/usuarios", json=user_data)
    
    resp_dup = client.post("/api/v1/usuarios", json=user_data)
    assert resp_dup.status_code == 400
    assert "Já existe uma conta" in resp_dup.json()["detail"]

def test_05_erro_401_unauthorized_sem_token(client):
    response = client.get("/api/v1/usuarios/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"] or "Token" in response.json()["detail"] or "credenciais" in response.json()["detail"]

def test_06_erro_401_unauthorized_token_invalido(client):
    headers = {"Authorization": "Bearer token_completamente_invalido_xyz123"}
    response = client.get("/api/v1/usuarios/me", headers=headers)
    assert response.status_code == 401

def test_07_erro_403_forbidden_atleta_tenta_listar_usuarios(client):
    client.post("/api/v1/usuarios", json={
        "nome": "Atleta Teste",
        "email": "atleta@bjj.com",
        "senha": "password123",
        "perfil": "atleta"
    })
    token = client.post("/api/v1/auth/login", data={"username": "atleta@bjj.com", "password": "password123"}).json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/usuarios", headers=headers)
    assert response.status_code == 403
    assert "Acesso negado" in response.json()["detail"]

def test_08_erro_403_forbidden_atleta_tenta_criar_evento(client):
    client.post("/api/v1/usuarios", json={
        "nome": "Mica Galvão",
        "email": "mica@bjj.com",
        "senha": "password123",
        "perfil": "atleta"
    })
    token = client.post("/api/v1/auth/login", data={"username": "mica@bjj.com", "password": "password123"}).json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    evento_payload = {
        "nome": "Campeonato Ilegal",
        "descricao": "Tentativa por atleta",
        "local_ginasio": "Ginásio X",
        "data_evento": (datetime.now() + timedelta(days=30)).isoformat(),
        "data_limite_inscricao": (datetime.now() + timedelta(days=20)).isoformat(),
        "data_checagem_geral": (datetime.now() + timedelta(days=25)).isoformat(),
        "qtd_tatames": 4,
        "regulamento": "IBJJF"
    }
    response = client.post("/api/v1/eventos", json=evento_payload, headers=headers)
    assert response.status_code == 403

def test_09_organizador_cria_evento_e_categoria(client):
    client.post("/api/v1/usuarios", json={
        "nome": "Federação Paulista BJJ",
        "email": "fpbjj@bjj.com",
        "senha": "password123",
        "perfil": "organizador"
    })
    token = client.post("/api/v1/auth/login", data={"username": "fpbjj@bjj.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    evento_payload = {
        "nome": "São Paulo Open 2026",
        "descricao": "Etapa Oficial FPBJJ",
        "local_ginasio": "Ginásio do Ibirapuera",
        "data_evento": (datetime.now() + timedelta(days=30)).isoformat(),
        "data_limite_inscricao": (datetime.now() + timedelta(days=20)).isoformat(),
        "data_checagem_geral": (datetime.now() + timedelta(days=25)).isoformat(),
        "qtd_tatames": 6,
        "regulamento": "IBJJF"
    }
    resp_ev = client.post("/api/v1/eventos", json=evento_payload, headers=headers)
    assert resp_ev.status_code == 201
    evento_id = resp_ev.json()["id"]

    cat_payload = {
        "modalidade": "Gi",
        "genero": "Masculino",
        "divisao_idade": "Adulto",
        "faixa": "Preta",
        "nome_categoria": "Pesadíssimo",
        "peso_limite_kg": 120.0
    }
    resp_cat = client.post(f"/api/v1/eventos/{evento_id}/categorias", json=cat_payload, headers=headers)
    assert resp_cat.status_code == 201
    assert resp_cat.json()["nome_categoria"] == "Pesadíssimo"

def test_10_fluxo_atleta_perfil_e_inscricao(client):
    client.post("/api/v1/usuarios", json={"nome": "CBJJ", "email": "cbjj@bjj.com", "senha": "123", "perfil": "organizador"})
    tok_org = client.post("/api/v1/auth/login", data={"username": "cbjj@bjj.com", "password": "123"}).json()["access_token"]
    h_org = {"Authorization": f"Bearer {tok_org}"}

    ev_id = client.post("/api/v1/eventos", json={
        "nome": "Brasileiro 2026",
        "local_ginasio": "Barueri",
        "data_evento": (datetime.now() + timedelta(days=30)).isoformat(),
        "data_limite_inscricao": (datetime.now() + timedelta(days=20)).isoformat(),
        "data_checagem_geral": (datetime.now() + timedelta(days=25)).isoformat()
    }, headers=h_org).json()["id"]

    cat_id = client.post(f"/api/v1/eventos/{ev_id}/categorias", json={
        "modalidade": "Gi", "genero": "Masculino", "divisao_idade": "Adulto", "faixa": "Preta", "nome_categoria": "Leve", "peso_limite_kg": 76.0
    }, headers=h_org).json()["id"]

    client.post("/api/v1/usuarios", json={"nome": "Kaynan Duarte", "email": "kaynan@bjj.com", "senha": "123", "perfil": "atleta"})
    tok_atleta = client.post("/api/v1/auth/login", data={"username": "kaynan@bjj.com", "password": "123"}).json()["access_token"]
    h_atleta = {"Authorization": f"Bearer {tok_atleta}"}

    client.post("/api/v1/atleta/perfil", json={
        "data_nascimento": "1998-01-01",
        "genero": "Masculino",
        "faixa": "Preta",
        "peso_atual_kg": 74.5,
        "academia_equipe": "Atos Jiu-Jitsu"
    }, headers=h_atleta)

    resp_insc = client.post("/api/v1/inscricoes", json={"categoria_id": cat_id}, headers=h_atleta)
    assert resp_insc.status_code == 201
    assert resp_insc.json()["status_pagamento"] == "Pago"
