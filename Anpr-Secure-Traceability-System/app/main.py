import cv2
import numpy as np
import jwt
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from ultralytics import YOLO
import easyocr

from .database import add_log_entry, init_db

app = FastAPI(title="ANPR Secure Access - Production Draft")

# --- CONFIGURATION ---
# Security keys (Production mein ye .env file se aani chahiye)
SECRET_KEY = "adani_rpi_secure_key" 
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

init_db() 
model = YOLO('yolov8m.pt') 
reader = easyocr.Reader(['en'], gpu=False) # Raspberry Pi CPU ke liye

def verify_token(token: str = Depends(oauth2_scheme)):
    """JWT Token verify karne ke liye security layer."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Security Token")

def run_anpr(frame):
    """Vehicle detection aur plate recognition ka logic."""
    results = model(frame, classes=[2, 3, 5, 7], conf=0.45, verbose=False)[0]
    output = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        v_type = {2:'Car', 3:'Bike', 5:'Bus', 7:'Truck'}.get(cls_id, "Unknown")

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = frame[y1:y2, x1:x2]
        
        ocr_out = reader.readtext(crop)
        plate = "".join(e for e in ocr_out[0][1].upper() if e.isalnum()) if ocr_out else "UNREAD"
        conf = round(float(ocr_out[0][2] * 100), 1) if ocr_out else 0.0
       
        status = "AUTHORIZED" if plate in ["OR01R0027", "ORDIR0027"] else "UNAUTHORIZED ALERT"
       
        add_log_entry(v_type, plate, status, conf)
        output.append({"vehicle": v_type, "plate": plate, "status": status})
        
    return output

# --- API ENDPOINTS ---
@app.post("/scan")
async def scan_vehicle(file: UploadFile = File(...), token: str = Depends(verify_token)):
    """Secured endpoint for real-time access control."""
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    results = run_anpr(frame)
    return {"gate": "GATE-01", "detections": results}