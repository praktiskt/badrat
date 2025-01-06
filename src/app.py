import json
import os

from fastapi import FastAPI, Request

import middleware
from badrat import Badrat

app = FastAPI()
app.middleware("http")(
    middleware.Badrat(
        on_endpoints=["/.*"],
        exclude_endpoints=["/health", "/slim", "/complete"],
    ),
)


BADRAT_INCLUDE = os.getenv(
    "BADRAT_INCLUDE",
    "method,url,query_params,headers,cookies,body",
)
br = Badrat(include_in_request=BADRAT_INCLUDE.lower().split(","))


@app.get("/health")
async def root():
    return {"Hello": "World"}


@app.get("/slim")
async def slim(request: Request):
    req = await br.parse_request(request)
    return br.baml.ClassifyDangerousSlim(json.dumps(req))


@app.get("/complete")
async def complete(request: Request):
    req = await br.parse_request(request)
    return br.baml.ClassifyDangerousComplete(json.dumps(req))


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"],
)
async def catch_all():
    return {}
