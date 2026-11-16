from pydantic import BaseModel
from datetime import date

class PerfilAtletaCreate(BaseModel):
    data_nascimento: date
    genero: str # Masculino / Feminino
    faixa: str # Branca, Azul, Roxa, Marrom, Preta
    peso_atual_kg: float
    academia_equipe: str

class PerfilAtletaResponse(BaseModel):
    id: int
    usuario_id: int
    data_nascimento: date
    genero: str
    faixa: str
    peso_atual_kg: float
    academia_equipe: str
    faixa_confirmada: bool

    class Config:
        from_attributes = True
