from fastapi import Request, Response
from typing import Callable
from fastapi.routing import APIRoute

class CustomRoute(APIRoute):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.body = await request.body()
            response = await original_route_handler(request)
            return response

        return custom_route_handler
