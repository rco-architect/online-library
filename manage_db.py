import sqlite3
import subprocess
import sys

DB_FILE = "local_library.db"
SQL_EXPORT = "schema.sql"
D1_DB_NAME = "my-library-db"

def init_local_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        cover_url TEXT NOT NULL,
        b2_key TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def export_to_sql():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    with open(SQL_EXPORT, "w", encoding="utf-8") as f:
        f.write("DROP TABLE IF EXISTS books;\n\n")
        f.write("CREATE TABLE books (\n")
        f.write("  id TEXT PRIMARY KEY,\n")
        f.write("  title TEXT NOT NULL,\n")
        f.write("  author TEXT NOT NULL,\n")
        f.write("  cover_url TEXT NOT NULL,\n")
        f.write("  b2_key TEXT NOT NULL\n")
        f.write(");\n\n")
        
        for row in rows:
            f.write(f"INSERT INTO books (id, title, author, cover_url, b2_key) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');\n")

def add_book():
    book_id = input("Enter Book ID (e.g., clean_code): ").strip()
    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    cover_url = input("Enter Cover Image URL: ").strip()
    b2_key = input("Enter Backblaze B2 File Key: ").strip()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?)",
            (book_id, title, author, cover_url, b2_key)
        )
        conn.commit()
        print(f"\n[+] Successfully added/updated '{title}' in local SQLite!")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        conn.close()

def sync_to_cloudflare():
    export_to_sql()
    print("\n[*] Pushing generated schema.sql to Cloudflare D1...")
    cmd = f"npx wrangler d1 execute {D1_DB_NAME} --remote --file=./{SQL_EXPORT}"
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print("[+] D1 database successfully synced!")
    else:
        print("[-] Sync failed. Check Wrangler authentication.")

def main():
    init_local_db()
    while True:
        print("\n=== LIBRARY DATABASE MANAGER ===")
        print("1. Add/Update Book")
        print("2. Export Local DB & Sync to Cloudflare D1")
        print("3. Exit")
        choice = input("Select option (1-3): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            sync_to_cloudflare()
        elif choice == "3":
            sys.exit(0)

if __name__ == "__main__":
    main()