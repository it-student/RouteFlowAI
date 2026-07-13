"""
This module is responsible for the postgres DB,
i.e. the connection, engine, execution of all CRUD operations.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

DB_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# import psycopg2 as c
#
# with c.connect(database = "postgres",
#                 user = "postgres",
#                 password =  "Banane1988",
#                 host = "localhost",
#                 port = 5431) as conn:
#     print("Connection established!")
