from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

import badrat
import baml_client

if TYPE_CHECKING:
    from fastapi import Request

    from baml_client.types import ResultComplete, ResultSlim


class Badrat:
    def __init__(
        self,
        on_endpoints: list[str],
        exclude_endpoints: list[str] | None = None,
        complete_analysis=False,
        badrat_client: badrat.Badrat = badrat.Badrat(),
    ) -> None:
        if exclude_endpoints is None:
            exclude_endpoints = []
        self.baml = baml_client.b
        self.br = badrat_client

        for pat in on_endpoints:
            re.compile(pat)  # raises exception on bad regex
        for pat in exclude_endpoints:
            re.compile(pat)  # raises exception on bad regex

        self.on_endpoints = on_endpoints
        self.exclude_endpoints = exclude_endpoints
        self.complete_analysis = complete_analysis

    def can_ignore_request(self, request: Request) -> bool:
        for pat in self.exclude_endpoints:
            if re.match(pat, request.url.path):
                return True

        return all(not re.match(pat, request.url.path) for pat in self.on_endpoints)

    async def check(self, request: Request) -> ResultSlim | ResultComplete:
        req = await self.br.parse_request(request)

        if self.complete_analysis:
            return self.baml.ClassifyDangerousComplete(json.dumps(req))

        return self.baml.ClassifyDangerousSlim(json.dumps(req))

    async def __call__(
        self,
        request: Request,
        call_next,
    ):
        if self.can_ignore_request(request):
            return await call_next(request)

        resp = await self.check(request)
        if resp.possibly_dangerous:
            return JSONResponse(content=resp.dict(), status_code=403)

        return await call_next(request)
