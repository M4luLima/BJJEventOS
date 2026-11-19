from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.luta import Luta
from app.schemas.luta import ResultadoLutaUpdate, LutaResponse
from app.core.deps import require_roles

router = APIRouter(tags=["Chaves & Lutas"])

@router.put("/lutas/{luta_id}/resultado", response_model=LutaResponse)
def lancar_resultado_luta(
    luta_id: int,
    resultado_in: ResultadoLutaUpdate,
    db: Session = Depends(get_db),
    organizador: Usuario = Depends(require_roles(["organizador", "admin"]))
):
    luta = db.query(Luta).filter(Luta.id == luta_id).first()
    if not luta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Luta não encontrada")
    
    luta.vencedor_id = resultado_in.vencedor_id
    luta.metodo_vitoria = resultado_in.metodo_vitoria
    luta.placar_detalhado = resultado_in.placar_detalhado
    
    db.commit()
    db.refresh(luta)
    return luta
