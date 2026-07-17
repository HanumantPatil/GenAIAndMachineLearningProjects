from fastapi import FastAPI
app = FastAPI()

# Use API_Model/run_dev.ps1 on Windows to avoid FastAPI CLI console encoding issues.
# .\API_Model\run_dev.ps1   
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/helloworld")
def read_helloworld():
    return {"Hello": "New World"}