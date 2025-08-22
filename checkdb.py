import os, psycopg2

u = os.environ.get("DATABASE_URL","").strip()
print("RAW starts:", u[:60])
# minimal normalization: scheme + ssl only
if u.lower().startswith("postgres://"):
    u = u.replace("postgres://","postgresql://",1)
if "sslmode=" not in u:
    u += ("&" if "?" in u else "?") + "sslmode=require"
print("CONNECTING…")
conn = psycopg2.connect(u, connect_timeout=5)
with conn.cursor() as cur:
    cur.execute("select current_user, current_database();")
    print("Connected as:", cur.fetchone())
conn.close()
print("OK")