from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inscricao import Inscricao
from app.models.categoria import Categoria
from app.models.perfil_atleta import PerfilAtleta
from app.models.usuario import Usuario
from app.schemas.inscricao import InscricaoCreate, InscricaoResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/inscricoes", tags=["Inscrições de Atletas"])

@router.post("", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def realizar_inscricao(
    inscricao_in: InscricaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.perfil != "atleta":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apenas atletas podem se inscrever.")
    
    perfil = db.query(PerfilAtleta).filter(PerfilAtleta.usuario_id == current_user.id).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cadastre sua ficha biométrica de atleta antes de se inscrever.")

    categoria = db.query(Categoria).filter(Categoria.id == inscricao_in.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")

    # RN07: Veto a inscrições duplicadas na mesma categoria
    insc_existente = db.query(Inscricao).filter(
        Inscricao.atleta_id == current_user.id,
        Inscricao.categoria_id == inscricao_in.categoria_id
    ).first()
    if insc_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Atleta já está inscrito nesta categoria.")

    # RN04: Controle de peso na inscrição
    if categoria.peso_limite_kg and perfil.peso_atual_kg > categoria.peso_limite_kg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Peso do atleta excede o limite da categoria.")

    nova_insc = Inscricao(
        atleta_id=current_user.id,
        categoria_id=inscricao_in.categoria_id,
        status_pagamento="Pago",
        status_pesagem="Aguardando"
    )
    db.add(nova_insc)
    db.commit()
    db.refresh(nova_insc)
    return nova_insc
