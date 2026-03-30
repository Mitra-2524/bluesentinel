from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import os
import sqlite3

router = APIRouter()


class Species(BaseModel):
    name: str
    scientific_name: str
    iucn_status: str
    breeding_season: str
    legal_status: str


# =======================
# SPECIES APIs
# =======================

@router.get("/species")
def get_species():
    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM species")
    rows = cursor.fetchall()
    conn.close()

    species_list = []

    for row in rows:
        species_list.append({
            "id": row[0],
            "name": row[1],
            "scientific_name": row[2],
            "iucn_status": row[3],
            "breeding_season": row[4],
            "legal_status": row[5]
        })

    return {"species": species_list}


@router.post("/species")
def add_species(species: Species):
    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS species (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        scientific_name TEXT,
        iucn_status TEXT,
        breeding_season TEXT,
        legal_status TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO species
    (name, scientific_name, iucn_status, breeding_season, legal_status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        species.name,
        species.scientific_name,
        species.iucn_status,
        species.breeding_season,
        species.legal_status
    ))

    conn.commit()
    conn.close()

    return {"message": "Species added successfully"}


@router.get("/species/check/{fish_name}")
def check_species(fish_name: str):

    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, scientific_name, iucn_status, breeding_season, legal_status
        FROM species
        WHERE LOWER(name)=LOWER(?)
        ORDER BY id DESC
        LIMIT 1
    """, (fish_name,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"message": "Species not found"}

    warning = ""

    if "restricted" in row[4].lower():
        warning = "⚠ Avoid catching this species during breeding season"

    elif "illegal" in row[4].lower():
        warning = "🚫 Catching this species is illegal"

    return {
        "name": row[0],
        "scientific_name": row[1],
        "iucn_status": row[2],
        "breeding_season": row[3],
        "legal_status": row[4],
        "warning": warning
    }


# =======================
# REPORT SYSTEM (FIXED)
# =======================

@router.post("/report")
async def report_illegal_fishing(
    species: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: str = Form(...),
    photo: UploadFile = File(None)
):

    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        latitude REAL,
        longitude REAL,
        description TEXT,
        photo TEXT
    )
    """)

    file_location = ""

    # ✅ FIXED: Only save photo if provided
    if photo:
        os.makedirs("uploads", exist_ok=True)
        file_location = f"uploads/{photo.filename}"

        with open(file_location, "wb") as f:
            f.write(await photo.read())

    cursor.execute("""
    INSERT INTO reports (species, latitude, longitude, description, photo)
    VALUES (?, ?, ?, ?, ?)
    """, (
        species,
        latitude,
        longitude,
        description,
        file_location
    ))

    conn.commit()
    conn.close()

    return {"message": "Report submitted successfully"}


@router.get("/reports")
def get_reports():

    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()
    conn.close()

    reports = []

    for row in rows:
        reports.append({
            "id": row[0],
            "species": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "description": row[4],
            "photo": row[5]
        })

    return {"reports": reports}

@router.get("/delete-report/{report_id}")
def delete_report(report_id: int):
    conn = sqlite3.connect("species.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))

    conn.commit()
    conn.close()

    return {"message": f"Report {report_id} deleted"}