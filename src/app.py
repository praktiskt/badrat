from fastapi import FastAPI

import middleware

app = FastAPI()
app.middleware("http")(middleware.Badrat())


@app.get("/")
async def root():
    return {"Hello": "World"}
