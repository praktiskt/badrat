from __future__ import annotations

import json
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import baml_client

if TYPE_CHECKING:
    from fastapi import Request


class Badrat:
    POSSIBLE_REQUEST_PARAMS = (
        "method",
        "url",
        "query_params",
        "headers",
        "body",
    )

    def __init__(
        self,
        include_in_request=(
            "method",
            "url",
            "query_params",
            "headers",
            "body",
        ),
    ) -> None:
        self.baml = baml_client.b

        for v in include_in_request:
            assert (
                v in self.POSSIBLE_REQUEST_PARAMS
            ), f"request parameter {v} is unknown"
        self.incl = include_in_request

    async def parse_request(self, request: Request):
        body = await request.body()

        result = {}
        if "method" in self.incl:
            result["method"] = request.method
        if "url" in self.incl:
            parsed_url = urlparse(str(request.url))
            result["url"] = {
                "scheme": parsed_url.scheme if parsed_url.scheme else None,
                "netloc": parsed_url.netloc if parsed_url.netloc else None,
                "path": parsed_url.path if parsed_url.path else None,
                "params": parsed_url.params if parsed_url.params else None,
                "fragment": parsed_url.fragment if parsed_url.fragment else None,
                "query": dict(request.query_params) if request.query_params else None,
            }
            result["url"] = {k: v for k, v in result["url"].items() if v is not None}
        if "headers" in self.incl and request.headers:
            result["headers"] = dict(request.headers)
        if "body" in self.incl and body:
            result["body"] = body.decode()

        return result

    async def analyze_slim(self, request: Request):
        req = await self.parse_request(request)
        return self.baml.ClassifyDangerousSlim(json.dumps(req))

    async def analyze_complete(self, request: Request):
        req = await self.parse_request(request)
        return self.baml.ClassifyDangerousComplete(json.dumps(req))
