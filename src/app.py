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
        exclude_endpoints=["/health", "/slim/.*", "/complete/.*", "/docs"],
        badrat_client=br,
    ),
)


@app.get("/health")
async def root():
    return {"health": "ok"}


@app.api_route(
    "/slim/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"],
)
async def slim(request: Request):
    return await br.analyze_slim(request)


@app.api_route(
    "/complete/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"],
)
async def complete(request: Request):
    return await br.analyze_complete(request)
