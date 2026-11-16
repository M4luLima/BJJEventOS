from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EventoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    local_ginasio: str
    data_evento: datetime
    data_limite_inscricao: datetime
    data_checagem_geral: datetime
    qtd_tatames: int = 4
    regulamento: str = "IBJJF"

class EventoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    local_ginasio: str
    data_evento: datetime
    data_limite_inscricao: datetime
    data_checagem_geral: datetime
    qtd_tatames: int
    regulamento: str
    organizador_id: int

    class Config:
        from_attributes = True
