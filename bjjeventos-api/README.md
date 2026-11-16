# BJJEventOS — API REST para Gerenciamento de Campeonatos de Jiu-Jitsu

API RESTful especializada para automação e gestão de campeonatos de Jiu-Jitsu (padrão IBJJF), desenvolvida em **Python 3.12**, **FastAPI**, **SQLAlchemy** e **PostgreSQL / SQLite**.

## 🥋 Perfis do Sistema (RBAC)
- **Admin:** Gestão global da plataforma, aprovação de organizadores e controle da tabela oficial IBJJF.
- **Organizador:** Cadastro de torneios, definição de tatames, fase de checagem geral, geração de chaves (*brackets*) e lançamento de resultados.
- **Atleta:** Perfil biométrico completo (Faixa, Peso corporal, Data de Nascimento, Gênero, Academia/Equipe), inscrição por categorias e acompanhamento de chamadas.

## 🚀 Tecnologias
- **Python 3.12 & FastAPI**
- **SQLAlchemy 2.0 & Alembic**
- **PyJWT & PBKDF2-HMAC-SHA256**
- **Pydantic v2 & Pytest**

Autora: **Maria Luiza**
