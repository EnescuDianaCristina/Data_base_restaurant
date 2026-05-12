import os   

import mariadb
import bcrypt
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
ROOT_USER = os.getenv("DB_USER")
ROOT_PASS = os.getenv("DB_PASSWORD")


def get_root_connection():
    return mariadb.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=ROOT_USER,
        password=ROOT_PASS,
        database=DB_NAME
    )



def hash_password(plain: str) -> str:
    return bcrypt.hashpw(
        plain.encode(),
        bcrypt.gensalt()
    ).decode()



def create_db_users():
    conn = get_root_connection()
    cur = conn.cursor()

    db_users = [
        ("manager", "manager123", "ALL PRIVILEGES"),
        ("insert_user", "insert123", "SELECT, INSERT"),
        ("update_user", "update123", "SELECT, INSERT, UPDATE"),
        ("delete_user", "delete123", "SELECT, DELETE")
    ]

    for username, password, privileges in db_users:
        try:
            cur.execute(f"DROP USER IF EXISTS '{username}'@'%'")
            cur.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            cur.execute(f"GRANT {privileges} ON {DB_NAME}.* TO '{username}'@'%'")
            print(f"[OK] Created DB user: {username}")
        except Exception as e:
            print("Error:", e)

    cur.execute("FLUSH PRIVILEGES")
    conn.commit()
    conn.close()



def encrypt_app_users():
    conn = get_root_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, password_hash FROM users")
    rows = cur.fetchall()

    for user_id, pwd in rows:

        if not str(pwd).startswith("$2b$"):
            hashed = hash_password(pwd)
            cur.execute(
                "UPDATE users SET password_hash=? WHERE id=?",
                (hashed, user_id)
            )
            print(f"[UPDATED] User ID {user_id} password encrypted")

    conn.commit()
    conn.close()

def encrypt_app_sku():
    conn = get_root_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, sku FROM mese_rezervate")
    rows = cur.fetchall()
    for row_id, sku in rows:

        if not str(sku).startswith("$2b$"):
            hashed = hash_password(str(sku))
            cur.execute(
                "UPDATE mese_rezervate SET sku=? WHERE id=?",
                (hashed, row_id)
            )
            print(f"[UPDATED] SKU {sku} encrypted")

    conn.commit()
    conn.close()

def main():
    print("\n=== CREATE DB USERS + GRANT ===")
    create_db_users()

    print("\n=== ENCRYPT APP USERS PASSWORDS ===")
    encrypt_app_users()

    print("\n=== ENCRYPT APP SKUS PASSWORDS ===")
    encrypt_app_sku()

    print("\n SECURITY SETUP COMPLETED")

if __name__ == "__main__":
    main()
