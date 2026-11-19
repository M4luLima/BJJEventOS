# BJJEventOS — API REST para Gerenciamento de Campeonatos de Jiu-Jitsu

Plataforma RESTful especializada na gestão de campeonatos de Jiu-Jitsu (padrão IBJJF/CBJJ), desenvolvida por **Maria Luiza** em **Python 3.15**, **FastAPI**, **SQLAlchemy** e **PostgreSQL / SQLite**.

---

## 🥋 Perfis de Acesso (RBAC)

- **Admin:** Controle global do sistema, credenciamento de organizadores e exclusão de eventos.
- **Organizador:** Cadastro de torneios, definição de tatames, encerramento da checagem, geração de chaves e lançamento de placares.
- **Atleta:** Ficha biométrica (Faixa, Peso, Idade, Academia), inscrição por categoria (Peso e Absoluto) e acompanhamento de chaves.

---

## ✨ Funcionalidades

- Cadastro e autenticação de usuários com JWT
- Controle de acesso por perfil (Admin, Organizador, Atleta)
- Cadastro de atletas com faixa, peso, idade e academia
- Criação e gerenciamento de eventos e categorias
- Inscrição de atletas por categoria (Peso e Absoluto)
- Geração de chaves de lutas
- Lançamento de placares e resultados

---

## 🛠️ Tecnologias

- Python 3.15
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic / Pydantic Settings
- Alembic
- PyJWT
- Passlib + Bcrypt
- Python-Multipart
- Pytest + HTTPX
- PostgreSQL / SQLite

---

## ⚙️ Instalação e Execução

### 1. Criar e ativar o ambiente virtual

```bash
py -m venv venv
.\venv\Scripts\Activate.ps1
### 2. Instalar as dependências
py -m pip install -r requirements.txt
### 3. Configurar as variáveis de ambiente
copy .env.example .env
Exemplo do arquivo `.env`:
DATABASE_URL=sqlite:///./bjjeventos.db
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
> Para usar PostgreSQL, troque o `DATABASE_URL` para:
> `postgresql://usuario:senha@localhost:5432/bjjeventos`

### 4. Iniciar o servidor
py -m uvicorn app.main:app --reload
Servidor rodando em: `http://127.0.0.1:8000`

Documentação Interativa (Swagger): `http://127.0.0.1:8000/docs`

Documentação alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

---

## 📡 Principais Endpoints
Método | Rota | Descrição
POST | `/auth/login` | Login e geração do token JWT
POST | `/auth/register` | Cadastro de novo usuário
GET | `/usuarios/` | Listar usuários
GET | `/atletas/` | Listar atletas
POST | `/atletas/` | Cadastrar atleta
GET | `/eventos/` | Listar eventos
POST | `/eventos/` | Criar novo evento
GET | `/inscricoes/` | Listar inscrições
POST | `/inscricoes/` | Criar inscrição
> Veja todas as rotas completas em: `http://127.0.0.1:8000/docs`

---

## 📁 Estrutura do Projeto
bjjeventos-api/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── deps.py
│   │   └── security.py
│   ├── models/
│   │   ├── atleta.py
│   │   ├── categoria.py
│   │   ├── evento.py
│   │   ├── inscricao.py
│   │   ├── luta.py
│   │   ├── perfil_atleta.py
│   │   └── usuario.py
│   ├── routers/
│   │   ├── atleta.py
│   │   ├── auth.py
│   │   ├── eventos.py
│   │   ├── inscricoes.py
│   │   └── usuarios.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── database.py
│   └── main.py
├── tests/
├── .env.example
├── requirements.txt
└── README.md
---

## ✅ Testes
py -m pytest
Para ver com mais detalhes:
py -m pytest -v
---

##  Autora

*Maria Luiza* - BJJEventOS
