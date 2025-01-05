import json

from fastapi import Request
from fastapi.responses import JSONResponse

import baml_client


class Badrat:
    def __init__(self) -> None:
        self.baml = baml_client.b

    async def parse_request(self, request: Request):
        body = await request.body()
        return {
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "cookies": dict(request.cookies),
            # "scope": dict(request.scope),
            "body": body.decode(),
        }

    async def __call__(
        self,
        request: Request,
        call_next,
    ):
        req = await self.parse_request(request)
        resp = self.baml.ClassifyDangerous(json.dumps(req))
        if resp.possibly_dangerous:
            return JSONResponse(resp.dict())

        return await call_next(request)
