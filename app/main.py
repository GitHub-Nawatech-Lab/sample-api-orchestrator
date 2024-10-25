from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from app.schemas.response import ValidationErrorSchema, SuccessSchema
from app.schemas.utils import bad_request_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.router import router

app = FastAPI(
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorSchema},
        status.HTTP_200_OK: {"model": SuccessSchema},
    }
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="codebase-gpt",
        version="0.0.1",
        description="chatgpt",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "/favicon.ico"}
    for key, value in openapi_schema["paths"].items():
        for method, response in value.items():
            response["responses"].pop("422", None)

    openapi_schema["components"]["schemas"].pop("HTTPValidationError")
    openapi_schema["components"]["schemas"].pop("ValidationError")

    openapi_schema["components"].update(
        {
            "securitySchemes": {
                "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "x-api-key"},
            }
        }
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc):
    errors = exc.errors()
    error_message = {}
    for error in errors:
        field = error.get("loc")[1]
        message = error.get("msg")
        data = {field: message}
        error_message.update(data)

    errors = {"errors": error_message}
    return bad_request_handler(errors)


@app.get("/")
async def index():
    return JSONResponse(
        content={
            "ok": True,
            "code": 200,
            "data": {"version": "0.0.1"},
            "message": "Success",
        }
    )


app.include_router(router.router, tags=["openAI skillset"])
