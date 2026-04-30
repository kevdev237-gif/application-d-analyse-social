from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# INIT DATABASE
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS survey")  # 🔥 FORCE RESET

    c.execute("""
        CREATE TABLE survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            level TEXT,
            field TEXT,
            social_hours INTEGER,
            main_network TEXT,
            usage_time TEXT,
            study_hours INTEGER,
            concentration TEXT,
            distraction TEXT,
            grades_impact TEXT,
            mental_fatigue TEXT,
            procrastination TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return render_template("home.html")

# FORM
@app.route('/form')
def form():
    return render_template("form.html")

# SUBMIT
@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO survey (
            age, level, field,
            social_hours, main_network, usage_time,
            study_hours, concentration, distraction,
            grades_impact, mental_fatigue, procrastination
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form['age'],
        request.form['level'],
        request.form['field'],
        request.form['social_hours'],
        request.form['main_network'],
        request.form['usage_time'],
        request.form['study_hours'],
        request.form['concentration'],
        request.form['distraction'],
        request.form['grades_impact'],
        request.form['mental_fatigue'],
        request.form['procrastination']
    ))

    conn.commit()
    conn.close()

    return redirect("/analyse")

# ANALYSE
@app.route('/analyse')
def analyse():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM survey")
    total = c.fetchone()[0]

    c.execute("SELECT AVG(social_hours) FROM survey")
    avg_social = c.fetchone()[0] or 0

    c.execute("SELECT AVG(study_hours) FROM survey")
    avg_study = c.fetchone()[0] or 0

    c.execute("SELECT grades_impact, COUNT(*) FROM survey GROUP BY grades_impact")
    rows = c.fetchall()

    impacts = dict(rows) if rows else {}

    conn.close()

    return render_template(
        "analyse.html",
        total=total,
        avg_social=round(avg_social, 2),
        avg_study=round(avg_study, 2),
        impacts=impacts
    )

# DATA TABLE
@app.route('/data')
def data():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM survey")
    rows = c.fetchall()
    conn.close()

    return render_template("data.html", rows=rows)

if __name__ == "__main__":
   if __name__ == "__main__":
    app.run()