import logging
import time
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.operations import add, subtract, multiply, divide

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Calculator")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@app.on_event("startup")
def startup_event():
    logger.info("FastAPI Calculator application started")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("FastAPI Calculator application stopped")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info("Incoming request: %s %s", request.method, request.url.path)

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled server error during request: %s %s", request.method, request.url.path)
        raise

    duration = time.time() - start_time
    logger.info(
        "Completed request: %s %s | status=%s | duration=%.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    logger.info("Home page requested")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "error": None},
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
        logger.error("Invalid form operation requested: %s", operation)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": None, "error": "Invalid operation"},
            status_code=400,
        )

    try:
        result = operations_map[operation](a, b)
        logger.info("Form calculation result: %s", result)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": result, "error": None},
        )
    except ValueError as exc:
        logger.exception("Form calculation error")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": None, "error": str(exc)},
            status_code=400,
        )


@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.get("/add")
def add_numbers(a: float, b: float):
    logger.info("Add endpoint called with a=%s, b=%s", a, b)
    result = add(a, b)
    logger.info("Add endpoint result=%s", result)
    return {"operation": "add", "a": a, "b": b, "result": result}


@app.get("/subtract")
def subtract_numbers(a: float, b: float):
    logger.info("Subtract endpoint called with a=%s, b=%s", a, b)
    result = subtract(a, b)
    logger.info("Subtract endpoint result=%s", result)
    return {"operation": "subtract", "a": a, "b": b, "result": result}


@app.get("/multiply")
def multiply_numbers(a: float, b: float):
    logger.info("Multiply endpoint called with a=%s, b=%s", a, b)
    result = multiply(a, b)
    logger.info("Multiply endpoint result=%s", result)
    return {"operation": "multiply", "a": a, "b": b, "result": result}


@app.get("/divide")
def divide_numbers(a: float, b: float):
    logger.info("Divide endpoint called with a=%s, b=%s", a, b)
    try:
        result = divide(a, b)
        logger.info("Divide endpoint result=%s", result)
        return {"operation": "divide", "a": a, "b": b, "result": result}
    except ValueError as exc:
        logger.exception("Divide endpoint error")
        raise HTTPException(status_code=400, detail=str(exc)) from exc