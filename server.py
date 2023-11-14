from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn

other_computer_address = ""

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/run_code")
async def run_code(request: CodeRequest):
    print(request.code)
    try:
        exec(request.code)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        #Making get request to 'get-cv-peak' endpoint
        response = requests.get('f{other_computer_address}/get-cv-peaks')
        response.raise_for_status() #Raises a HTTPError if the status is 4xx, 5xxx
        return response.json()
    except request.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
# 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)