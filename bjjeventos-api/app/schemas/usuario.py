from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    perfil: str
    usuario_id: int

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: str = "atleta" # admin, organizador, atleta

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str
    criado_em: datetime

    class Config:
        from_attributes = True
