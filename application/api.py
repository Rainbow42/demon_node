from fastapi import APIRouter

from conveir.endpoints import router as conveir_router

router = APIRouter()

router.include_router(conveir_router)
