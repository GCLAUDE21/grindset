from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Grindset API is running"}

@app.get("/status")
def status():
    return {"status": "ok", "version": "1.0"}