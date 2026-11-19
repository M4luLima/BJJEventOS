from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.inscricao import Inscricao
from app.schemas.inscricao import InscricaoCreate, InscricaoResponse
from app.core.deps import require_roles

router = APIRouter(prefix="/inscricoes", tags=["Inscrições no Campeonato"])

@router.post("", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def realizar_inscricao(
    inscricao_in: InscricaoCreate,
    db: Session = Depends(get_db),
    atleta: Usuario = Depends(require_roles(["atleta"]))
):
    if not atleta.perfil_atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil de atleta não preenchido. Preencha seus dados de peso e faixa primeiro."
        )
    
    categoria = db.query(Categoria).filter(Categoria.id == inscricao_in.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")

    # RN07: Veto a Inscrições Duplicadas
    ja_inscrito = db.query(Inscricao).filter(
        Inscricao.atleta_id == atleta.id,
        Inscricao.categoria_id == categoria.id
    ).first()
    if ja_inscrito:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Atleta já está inscrito nesta categoria."
        )

    # RN04: Controle de Peso na Inscrição
    if categoria.peso_limite_kg and atleta.perfil_atleta.peso_atual_kg > categoria.peso_limite_kg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Peso do atleta ({atleta.perfil_atleta.peso_atual_kg}kg) excede o limite da categoria ({categoria.peso_limite_kg}kg)."
        )

    nova_inscricao = Inscricao(
        atleta_id=atleta.id,
        categoria_id=categoria.id,
        status_pagamento="Pago",
        status_pesagem="Aguardando"
    )
    db.add(nova_inscricao)
    db.commit()
    db.refresh(nova_inscricao)
    return nova_inscricao
