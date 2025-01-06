import json

from fastapi import Request
from fastapi.responses import JSONResponse

import badrat
import baml_client


class Badrat:
    def __init__(self) -> None:
        self.baml = baml_client.b
        self.br = badrat.Badrat()

    async def __call__(
        self,
        request: Request,
        call_next,
    ):
        req = await self.br.parse_request(request)
        resp = self.baml.ClassifyDangerousComplete(json.dumps(req))
        if resp.possibly_dangerous:
            return JSONResponse(resp.dict())

        return await call_next(request)
