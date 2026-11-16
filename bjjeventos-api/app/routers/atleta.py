from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.perfil_atleta import PerfilAtleta
from app.schemas.perfil_atleta import PerfilAtletaCreate, PerfilAtletaResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/atleta", tags=["Ficha de Atleta"])

@router.post("/perfil", response_model=PerfilAtletaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_perfil_atleta(
    perfil_in: PerfilAtletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.perfil != "atleta":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apenas contas do tipo atleta podem cadastrar ficha esportiva.")
    
    perfil_existente = db.query(PerfilAtleta).filter(PerfilAtleta.usuario_id == current_user.id).first()
    if perfil_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Atleta já possui perfil cadastrado.")

    novo_perfil = PerfilAtleta(
        usuario_id=current_user.id,
        data_nascimento=perfil_in.data_nascimento,
        genero=perfil_in.genero,
        faixa=perfil_in.faixa,
        peso_atual_kg=perfil_in.peso_atual_kg,
        academia_equipe=perfil_in.academia_equipe
    )
    db.add(novo_perfil)
    db.commit()
    db.refresh(novo_perfil)
    return novo_perfil

@router.get("/perfil", response_model=PerfilAtletaResponse)
def obter_perfil_atleta(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    perfil = db.query(PerfilAtleta).filter(PerfilAtleta.usuario_id == current_user.id).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ficha de atleta não cadastrada.")
    return perfil
