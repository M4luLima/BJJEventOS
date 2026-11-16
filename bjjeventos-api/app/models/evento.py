from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    local_ginasio = Column(String(150), nullable=False)
    data_evento = Column(DateTime, nullable=False)
    data_limite_inscricao = Column(DateTime, nullable=False)
    data_checagem_geral = Column(DateTime, nullable=False)
    qtd_tatames = Column(Integer, default=4)
    regulamento = Column(String(50), default="IBJJF")
    organizador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    categorias = relationship("Categoria", back_populates="evento", cascade="all, delete-orphan")
