import pandas as pd
import sqlite3

# read Excel dataset
data = pd.read_excel("fish_species_data.xlsx")

print(data.columns) 

conn = sqlite3.connect("species.db")
cursor = conn.cursor()

# create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS species (
    id INTEGER PRIMARY KEY,
    name TEXT,
    scientific_name TEXT,
    iucn_status TEXT,
    breeding_season TEXT,
    legal_status TEXT
)
""")

# insert rows
for _, row in data.iterrows():
    cursor.execute("""
    INSERT INTO species
    (name, scientific_name, iucn_status, breeding_season, legal_status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        row["name"],
        row["scientific_name"],
        row["iucn_status"],
        row["breeding_season"],
        row["legal_status"]
    ))

conn.commit()
conn.close()

print("Species dataset imported successfully")
