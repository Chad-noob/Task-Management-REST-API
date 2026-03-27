from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .init_db import initialize_database
from .routes.auth_routes import router as auth_router
from .routes.task_routes import router as task_router

app = FastAPI(
    title='Task Management REST API',
    version='1.0.0',
    description='A small task manager API built for an assessment submission.',
)


@app.on_event('startup')
def on_startup() -> None:
    initialize_database()


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            'success': False,
            'message': 'Request validation failed',
            'errors': [
                {
                    'field': '.'.join(str(part) for part in error['loc'][1:]),
                    'message': error['msg'],
                }
                for error in exc.errors()
            ],
        },
    )


@app.exception_handler(HTTPException)
async def handle_http_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'message': exc.detail,
        },
    )


@app.get('/')
def home():
    return {
        'success': True,
        'message': 'Task Management REST API is up and running',
    }


app.include_router(auth_router)
app.include_router(task_router)
