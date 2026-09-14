import logging

from fastapi import FastAPI, HTTPException

from app.db import get_connection

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    return {"message": "NIC AWS Fargate RDS App"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-health")
def database_health_check():
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        connection.close()

        return {
            "status": "ok",
            "database": "connected",
            "result": result[0],
        }

    except Exception:
        logger.exception("Database connection failed")
        raise HTTPException(
            status_code=500,
            detail="Database connection failed",
        )