import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://your_username:your_password@localhost:5432/your_database' # setup your database
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
