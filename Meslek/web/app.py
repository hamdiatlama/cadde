import os, json
from flask import Flask, render_template, request, g

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_PG = "postgres" in DATABASE_URL

if USE_PG:
    import psycopg2, psycopg2.extras
    def get_db():
        if "db" not in g:
            g.db = psycopg2.connect(DATABASE_URL)
            g.db.autocommit = True
        return g.db
else:
    import sqlite3
    DB_PATH = os.path.join(os.path.dirname(__file__), "meslekler.db")
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(DB_PATH)
            g.db.row_factory = sqlite3.Row
        return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    db = get_db()
    if USE_PG:
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, name VARCHAR(200) NOT NULL, emoji VARCHAR(10), sort_order INT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS professions (id SERIAL PRIMARY KEY, name VARCHAR(200) NOT NULL, category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_pn ON professions(name)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_pc ON professions(category_id)")
        db.commit()
    else:
        db.executescript("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT, emoji TEXT, sort_order INTEGER); CREATE TABLE IF NOT EXISTS professions (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER REFERENCES categories(id)); CREATE INDEX IF NOT EXISTS idx_pn ON professions(name); CREATE INDEX IF NOT EXISTS idx_pc ON professions(category_id);")
        db.commit()

def import_data():
    db = get_db()
    if db.execute("SELECT COUNT(*) FROM categories").fetchone()[0] > 0:
        return
    with open(os.path.join(os.path.dirname(__file__), "data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    if USE_PG:
        for c in data["categories"]:
            db.execute("INSERT INTO categories (id, name, emoji, sort_order) VALUES (%s,%s,%s,%s)", (c["id"], c["name"], c["emoji"], c["sort_order"]))
        for p in data["professions"]:
            db.execute("INSERT INTO professions (id, name, category_id) VALUES (%s,%s,%s)", (p["id"], p["name"], p["category_id"]))
    else:
        for c in data["categories"]:
            db.execute("INSERT INTO categories VALUES (?,?,?,?)", (c["id"], c["name"], c["emoji"], c["sort_order"]))
        for p in data["professions"]:
            db.execute("INSERT INTO professions VALUES (?,?,?)", (p["id"], p["name"], p["category_id"]))
    db.commit()

def q(sql, params=None, one=False):
    db = get_db()
    if USE_PG:
        c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute(sql, params or ())
        return c.fetchone() if one else c.fetchall()
    cur = db.execute(sql, params or ())
    return cur.fetchone() if one else cur.fetchall()

@app.route("/")
def index():
    cats = q("SELECT c.*, (SELECT COUNT(*) FROM professions WHERE category_id=c.id) as cnt FROM categories c ORDER BY sort_order")
    total = q("SELECT COUNT(*) as cnt FROM professions", one=True)["cnt"]
    return render_template("index.html", categories=cats, total=total)

@app.route("/kategori/<int:cid>")
def category(cid):
    cat = q("SELECT * FROM categories WHERE id=" + ("%s" if USE_PG else "?"), (cid,), one=True)
    if not cat:
        return "Bulunamadi", 404
    profs = q("SELECT * FROM professions WHERE category_id=" + ("%s" if USE_PG else "?") + " ORDER BY name", (cid,))
    return render_template("category.html", category=cat, professions=profs)

@app.route("/arama")
def search():
    q_str = request.args.get("q", "").strip()
    results = []
    if q_str:
        like = f"%{q_str}%"
        if USE_PG:
            results = q("SELECT p.*, c.name as cn, c.emoji FROM professions p JOIN categories c ON p.category_id=c.id WHERE p.name ILIKE %s ORDER BY p.name", (like,))
        else:
            results = q("SELECT p.*, c.name as cn, c.emoji FROM professions p JOIN categories c ON p.category_id=c.id WHERE p.name LIKE ? ORDER BY p.name", (like,))
    return render_template("search.html", query=q_str, results=results)

@app.route("/api/kategoriler")
def api_cats():
    return [dict(r) for r in q("SELECT id, name, emoji FROM categories ORDER BY sort_order")]

@app.route("/api/meslekler")
def api_profs():
    cid = request.args.get("category_id", type=int)
    if cid:
        return [dict(r) for r in q("SELECT id, name FROM professions WHERE category_id=" + ("%s" if USE_PG else "?") + " ORDER BY name", (cid,))]
    return [dict(r) for r in q("SELECT p.id, p.name, c.name as cat_name FROM professions p JOIN categories c ON p.category_id=c.id ORDER BY p.name")]

if __name__ == "__main__":
    with app.app_context():
        init_db()
        import_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
