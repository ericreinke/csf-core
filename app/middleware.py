import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Base logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("csf_core")

def setup_middleware(app: FastAPI):
    """Register all middleware and global exception handlers to the FastAPI app."""
    
    # Global Request Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Determine log level based on response status code
            log_msg = f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s"
            if response.status_code >= 500:
                logger.error(f"Server Error - {log_msg}")
            elif response.status_code >= 400:
                logger.warning(f"Client Error - {log_msg}")
            else:
                logger.info(f"Success - {log_msg}")
                
            return response
        except Exception as e:
            # If an exception blows past the exception handlers
            process_time = time.time() - start_time
            logger.exception(f"Unhandled failure during {request.method} {request.url.path} after {process_time:.4f}s")
            raise

    # Exception handler for expected HTTP errors (4xx, 5xx thrown intentionally)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP Exception {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    # Exception handler for Pydantic validation errors (422)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation Error on {request.method} {request.url.path}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()}
        )

    # Catch-all exception handler for 500 Internal Server Errors
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unexpected error during {request.method} {request.url.path}:\n{exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )
