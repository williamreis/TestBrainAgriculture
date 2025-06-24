import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import produtor, propriedade, safra, cultura, propriedade_safra_cultura, dashboard
from app.utils.logger import log_api_request, log_error

"""
 Configuração da aplicação FastAPI 
"""
app = FastAPI(title="TestBrainAgriculture API")

"""
Configurar CORS
- Permitir todas as origens, métodos e cabeçalhos
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logs
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        # Log da requisição
        log_api_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=duration
        )

        return response
    except Exception as e:
        duration = time.time() - start_time
        log_error(e, f"Request {request.method} {request.url.path}")
        raise


app.include_router(produtor.router)
app.include_router(propriedade.router)
app.include_router(safra.router)
app.include_router(cultura.router)
app.include_router(propriedade_safra_cultura.router)
app.include_router(dashboard.router)

"""
Rota raiz
"""


@app.get("/")
def root():
    return {"message": "TestBrainAgriculture API", "docs": "/docs", "version": "0.1.5"}


"""
Rota de health check
"""


@app.get("/health")
def health_check():
    return {"status": "ok"}
