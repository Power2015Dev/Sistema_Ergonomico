import psycopg2 as pg
from dotenv import load_dotenv
import os

load_dotenv()
def Connect():
    # Cada vez que necesites hablar con la BD, llamas a esta función
    conexion = pg.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conexion