import json
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlmodel import SQLModel,select,Field,Sequence
from pydantic import BaseModel
from typing import Union

from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/Portfoilo"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data_from_json(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            data = json.load(f)
            print(len(data))
            return data
    except FileNotFoundError:
        print("File Not found")
        return []

SKILLS_DATA = load_data_from_json(Path(__file__).parent / "data" / "skills.json")
IMG_DATA = Path(__file__).parent / "img"

@app.get("/api/skills")
def log_skills():
    return SKILLS_DATA

@app.get("/img/{filename}")
def get_my_img(filename:str):
    file_path = IMG_DATA / filename
    print(f"Requesting file: {filename}")
    if not file_path.exists():
        return {"ERROR" : "Img not found"}
    return FileResponse(file_path)
