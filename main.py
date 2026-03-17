import logging
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.operations import add, subtract, multiply, divide

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Calculator")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    logger.info("Home page requested")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None,
            "selected_operation": "add",
        },
    )


@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    request: Request,
    a: float = Form(...),
    b: float = Form(...),
    operation: str = Form(...),
):
    logger.info("Form calculation requested: a=%s, b=%s, operation=%s", a, b, operation)

    operations_map = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if operation not in operations_map:
        logger.error("Invalid form operation: %s", operation)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "Invalid operation",
                "selected_operation": operation,
            },
            status_code=400,
        )

    try:
        result = operations_map[operation](a, b)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result,
                "error": None,
                "selected_operation": operation,
            },
        )
    except ValueError as exc:
        logger.exception("Form calculation error")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(exc),
                "selected_operation": operation,
            },
            status_code=400,
        )


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.get("/add")
def add_numbers(a: float, b: float):
    logger.info("Add endpoint called: %s + %s", a, b)
    return {"operation": "add", "a": a, "b": b, "result": add(a, b)}


@app.get("/subtract")
def subtract_numbers(a: float, b: float):
    logger.info("Subtract endpoint called: %s - %s", a, b)
    return {"operation": "subtract", "a": a, "b": b, "result": subtract(a, b)}


@app.get("/multiply")
def multiply_numbers(a: float, b: float):
    logger.info("Multiply endpoint called: %s * %s", a, b)
    return {"operation": "multiply", "a": a, "b": b, "result": multiply(a, b)}


@app.get("/divide")
def divide_numbers(a: float, b: float):
    logger.info("Divide endpoint called: %s / %s", a, b)
    try:
        return {"operation": "divide", "a": a, "b": b, "result": divide(a, b)}
    except ValueError as exc:
        logger.exception("Divide endpoint error")
        raise HTTPException(status_code=400, detail=str(exc)) from exc