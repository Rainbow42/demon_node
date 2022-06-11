import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application import api, settings


logging.basicConfig(format='%(levelname)s:     %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(
    title='Сервис Демон',
    docs_url=settings.BASE_API_URL + '/swagger/'
)
data = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix=settings.BASE_API_URL)


if __name__ == "__main__":
    uvicorn.run("main:app",
                loop="uvloop",
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                reload=True)
