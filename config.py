import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:2002sidomulyo@localhost:5432/tubes_sig'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False