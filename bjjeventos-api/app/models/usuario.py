from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False, default="atleta") # admin, organizador, atleta
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    perfil_atleta = relationship("PerfilAtleta", back_populates="usuario", uselist=False)
    inscricoes = relationship("Inscricao", back_populates="atleta")
