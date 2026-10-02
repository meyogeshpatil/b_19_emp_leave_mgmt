import psycopg2 # syncrhonous and blocking postgres driver/ asyncpg
from pathlib import Path

DATABASE_URL = "postgres://avnadmin:AVNS_pxGJZ4sGPHkApLDIiNB@pg-99fa075-mepatilyogesh-7e4a.j.aivencloud.com:10496/leave_mgmt?sslmode=require"
CA_PATH = Path(__file__).resolve().parent/"ca.pem"
def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='verify-full', sslrootcert = str(CA_PATH))


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()