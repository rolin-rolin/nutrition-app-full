#!/usr/bin/env python3

from app.db.session import engine
from app.db.models import Base

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables() 