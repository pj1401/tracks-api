from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from Tracks API!"}


@app.get("/api/v1/health")
async def health():
    return {"status": 200, "message": "OK"}
