from pydantic import BaseModel


class ValidationErrorSchema(BaseModel):
    ok: bool
    code: int
    errors: dict
    message: str


class SuccessSchema(BaseModel):
    ok: bool
    code: int
    data: dict
    message: str
