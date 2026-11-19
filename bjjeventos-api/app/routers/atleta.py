from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario, PerfilAtleta
from app.schemas.usuario import PerfilAtletaCreate, PerfilAtletaResponse
from app.core.deps import get_current_user, require_roles

router = APIRouter(prefix="/atleta", tags=["Perfil do Atleta"])

@router.post("/perfil", response_model=PerfilAtletaResponse, status_code=status.HTTP_201_CREATED)
def criar_perfil_atleta(
    perfil_in: PerfilAtletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["atleta"]))
):
    if current_user.perfil_atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui um perfil de atleta cadastrado."
        )
    
    perfil = PerfilAtleta(
        usuario_id=current_user.id,
        data_nascimento=perfil_in.data_nascimento,
        genero=perfil_in.genero,
        faixa=perfil_in.faixa,
        peso_atual_kg=perfil_in.peso_atual_kg,
        academia_equipe=perfil_in.academia_equipe
    )
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil

@router.get("/perfil", response_model=PerfilAtletaResponse)
def consultar_perfil_atleta(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if not current_user.perfil_atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não cadastrado para esta conta."
        )
    return current_user.perfil_atleta

@router.put("/perfil", response_model=PerfilAtletaResponse)
def atualizar_perfil_atleta(
    perfil_in: PerfilAtletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["atleta"]))
):
    perfil = current_user.perfil_atleta
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta ainda não cadastrado."
        )
    
    perfil.data_nascimento = perfil_in.data_nascimento
    perfil.genero = perfil_in.genero
    perfil.faixa = perfil_in.faixa
    perfil.peso_atual_kg = perfil_in.peso_atual_kg
    perfil.academia_equipe = perfil_in.academia_equipe
    
    db.commit()
    db.refresh(perfil)
    return perfil
