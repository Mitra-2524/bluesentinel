from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    scientific_name = Column(String)
    iucn_status = Column(String)
    breeding_season = Column(String)
    legal_status = Column(String)