from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    modalidade: str # Gi, No-Gi
    genero: str # Masculino, Feminino
    divisao_idade: str # Adulto, Master 1, etc.
    faixa: str # Branca, Azul, Roxa, Marrom, Preta
    nome_categoria: str # Leve, Pesado, Absoluto
    peso_limite_kg: Optional[float] = None

class CategoriaResponse(BaseModel):
    id: int
    evento_id: int
    modalidade: str
    genero: str
    divisao_idade: str
    faixa: str
    nome_categoria: str
    peso_limite_kg: Optional[float]

    class Config:
        from_attributes = True
