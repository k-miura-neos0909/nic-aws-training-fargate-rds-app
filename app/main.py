import logging

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_connection

app = FastAPI()

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def read_root(request: Request):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, message, created_at
                FROM messages
                ORDER BY id DESC
                """
            )
            messages = cursor.fetchall()

    finally:
        connection.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"messages": messages},
    )


@app.post("/messages")
def create_message(message: str = Form(...)):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (message) VALUES (%s)",
                (message,),
            )

        connection.commit()

    finally:
        connection.close()

    logger.info("Message registered")

    return RedirectResponse(url="/", status_code=303)


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