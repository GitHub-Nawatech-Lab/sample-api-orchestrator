from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from app.settings import settings

import time


class ApiKeyMiddleware(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            credentials_exception = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "ok": False,
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Unauthorized",
                },
            )

            # x_api_key = request.headers.get("x-api-key")

            # if x_api_key != settings.API_KEY:
            #     return credentials_exception

            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            return response

        return custom_route_handler
