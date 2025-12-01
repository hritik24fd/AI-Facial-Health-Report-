from fastapi import FastAPI,UploadFile,File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import numpy as np
from engine import analyze_face
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates =Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("webcam_ui.html",{"request": request})

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = np.array(img)
    
    
    result = analyze_face(img)
    if result is None:
        return {"error": "Could not analyze face in image"}
    
    return result