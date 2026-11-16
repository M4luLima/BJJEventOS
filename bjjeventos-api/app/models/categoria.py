from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    modalidade = Column(String(10), nullable=False) # Gi, No-Gi
    genero = Column(String(10), nullable=False) # Masculino, Feminino
    divisao_idade = Column(String(30), nullable=False) # Adulto, Master 1, etc.
    faixa = Column(String(20), nullable=False) # Branca, Azul, etc.
    nome_categoria = Column(String(30), nullable=False) # Leve, Pesado, Absoluto
    peso_limite_kg = Column(Float, nullable=True) # NULL para Absoluto

    evento = relationship("Evento", back_populates="categorias")
    inscricoes = relationship("Inscricao", back_populates="categoria")
    lutas = relationship("Luta", back_populates="categoria")
