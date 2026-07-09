from fastapi import FastAPI

app = FastAPI(title="AcousticSpace API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
