from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.evento import Evento
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.core.deps import require_roles

router = APIRouter(tags=["Categorias de Luta"])

@router.get("/eventos/{evento_id}/categorias", response_model=List[CategoriaResponse])
def listar_categorias_evento(evento_id: int, db: Session = Depends(get_db)):
    return db.query(Categoria).filter(Categoria.evento_id == evento_id).all()

@router.post("/eventos/{evento_id}/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria_evento(
    evento_id: int,
    categoria_in: CategoriaCreate,
    db: Session = Depends(get_db),
    organizador: Usuario = Depends(require_roles(["organizador", "admin"]))
):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campeonato não encontrado")
    
    nova_cat = Categoria(
        evento_id=evento_id,
        modalidade=categoria_in.modalidade,
        genero=categoria_in.genero,
        divisao_idade=categoria_in.divisao_idade,
        faixa=categoria_in.faixa,
        nome_categoria=categoria_in.nome_categoria,
        peso_limite_kg=categoria_in.peso_limite_kg
    )
    db.add(nova_cat)
    db.commit()
    db.refresh(nova_cat)
    return nova_cat
