import json
import os

from fastapi import FastAPI, Request

import middleware
from badrat import Badrat

BADRAT_INCLUDE = os.getenv(
    "BADRAT_INCLUDE",
    "method,url,query_params,headers,cookies,body",
)
br = Badrat(include_in_request=BADRAT_INCLUDE.lower().split(","))

app = FastAPI()
app.middleware("http")(
    middleware.Badrat(
        # on_endpoints=["/.*"], # default
        exclude_endpoints=["/health", "/slim", "/complete"],
        badrat_client=br,
    ),
)


@app.get("/health")
async def root():
    return {"health": "ok"}


@app.get("/slim")
async def slim(request: Request):
    req = await br.parse_request(request)
    return br.baml.ClassifyDangerousSlim(json.dumps(req))


@app.get("/complete")
async def complete(request: Request):
    req = await br.parse_request(request)
    return br.baml.ClassifyDangerousComplete(json.dumps(req))


@app.api_route(
    "/proxy/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"],
)
async def catch_all():
    return {}
