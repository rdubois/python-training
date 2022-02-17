import logging
from logging.config import fileConfig

from fastapi import FastAPI, Response, status

app = FastAPI()

fileConfig('src/analytic/logging.conf')
logger = logging.getLogger()

@app.get("/ready")
async def ready():
    logger.debug("Readiness probe called.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/alive")
async def alive():
    logger.debug("Liveness probe called.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)