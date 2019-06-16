import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

db_engine = create_engine(DATABASE_URL)
db_connection = db_engine.connect()
