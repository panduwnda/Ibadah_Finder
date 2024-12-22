import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:adam31@localhost:5432/tubes'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
