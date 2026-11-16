from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth, usuarios, eventos, inscricoes, lutas

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful para Gerenciamento de Campeonatos de Jiu-Jitsu (BJJEventOS)"
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(usuarios.router, prefix=settings.API_V1_STR)
app.include_router(eventos.router, prefix=settings.API_V1_STR)
app.include_router(inscricoes.router, prefix=settings.API_V1_STR)
app.include_router(lutas.router, prefix=settings.API_V1_STR)

@app.get("/")
def health_check():
    return {"status": "online", "app": settings.PROJECT_NAME, "version": settings.VERSION}
