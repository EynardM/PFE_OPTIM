from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util.objects import *
from main import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/run-main")
def run_main():
    journey, evaluation, storehouse = main()
    return {"journey": journey.to_dict(), "evaluation": evaluation, "storehouse": storehouse.to_dict()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
