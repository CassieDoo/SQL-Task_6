import os
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy.orm import sessionmaker


load_dotenv()

drivername = os.getenv("DRIVERNAME")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

DSN = f"{drivername}://{username}:{password}@{host}:{port}/{database}"

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
