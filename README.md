# ANPR-Based Secure Vehicle Access & Traceability System
**Target Hardware:** Raspberry Pi (ARM64) | **Project Status:** Active Development (Draft v0.1)

## Project Overview
This project is an automated vehicle entry management system designed for high-security industrial sites (e.g., Ports, Logistics Hubs). It replaces manual registers with an AI-driven digital audit trail, ensuring every entry is secure and traceable.

## Tech Stack
* **AI Engine:** YOLOv8m (Vehicle Classification) & EasyOCR (Plate Recognition).
* **Backend:** FastAPI with JWT (JSON Web Token) Authentication.
* **Database:** SQLite for persistent, tamper-evident access logs.
* **Deployment:** Dockerized for environment consistency on Edge hardware.

## Security & Traceability Features
* **Stateless Auth:** Uses JWT to secure API endpoints, ensuring only authorized personnel can access logs.
* **Audit Trail:** Every detection is logged with a timestamp, confidence score, and vehicle type in a local SQL database.
* **Edge-Optimized:** Configured to run on Raspberry Pi CPU using `opencv-python-headless` and `slim` Docker images.

## Project Status & Implementation Details

### Currently Implemented (Core Engine)
- **AI Pipeline:** Fully functional YOLOv8m detection and EasyOCR character recognition.
- **Data Persistence:** SQLite database integration for automated, tamper-evident logging of every vehicle entry.
- **Security Layer:** FastAPI backend with JWT authentication logic to protect access logs.
- **Environment:** Dockerfile configured for ARM64/Raspberry Pi architecture.

### Evidence of Work
#### 1. Real-Time Detection
Below is a sample of the system identifying a vehicle and extracting the license plate for authorization check.
<img width="482" height="698" alt="detection_sample1" src="https://github.com/user-attachments/assets/6347db60-a774-403b-a10d-dfaa36e89b5a" />

#### 2. Security Audit Logs (SQLite)
The system automatically populates the `security_audit.db`. Snapshot of structured traceability data:

| Timestamp | Vehicle Type | Plate Number | Status | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-23 10:15:22 | Truck | OR01R0027 | AUTHORIZED | 94.2% |
| 2026-04-23 10:18:45 | Car | MH12AB1234 | UNAUTHORIZED | 88.5% |

## Roadmap (Future Development)
The system is currently a functional prototype. Future development includes:
1. **Async DB Operations:** Moving to asynchronous writes to handle high-traffic gates.
2. **GPIO Integration:** Linking authorized detections to physical boom-barrier controls via Raspberry Pi pins.
3. **Hardware Benchmarking:** Comparing TensorRT vs. ONNX performance on the Pi's CPU.
4. **Secret Management:** Moving static keys to `.env` files for enterprise-grade security.

## Getting Started
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/Anpr-Secure-Traceability-System.git](https://github.com/your-username/Anpr-Secure-Traceability-System.git)
