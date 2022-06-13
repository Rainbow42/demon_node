from fastapi import APIRouter

from conveir.endpoints import router as conveir_router
from repositories.endpoints import router as repositories_router
# from pipeline.endpoints import router as repositories_router

router = APIRouter()

router.include_router(conveir_router)
router.include_router(repositories_router)
