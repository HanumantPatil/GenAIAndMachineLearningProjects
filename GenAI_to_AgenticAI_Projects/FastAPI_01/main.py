from fastapi import FastAPI

app = FastAPI()

# fastapi run .\FastAPI_01\main.py
@app.get("/")
async def root():
    return {"message": "Hello World"}