from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# =======================
# CORS (VERY IMPORTANT)
# =======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# DATA MODEL
# =======================
class Report(BaseModel):
    species: str
    latitude: float
    longitude: float
    description: str

# =======================
# IN-MEMORY STORAGE
# =======================
reports = []

# =======================
# ADD REPORT
# =======================
@app.post("/reports")
def add_report(report: Report):
    new_report = report.dict()
    new_report["id"] = len(reports) + 1
    reports.append(new_report)
    return {"message": "Report added successfully"}

# =======================
# GET ALL REPORTS
# =======================
@app.get("/reports")
def get_reports():
    return {"reports": reports}

# =======================
# ROOT CHECK
# =======================
@app.get("/")
def root():
    return {"message": "BlueSentinel API Running 🚀"}