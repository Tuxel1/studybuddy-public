from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import numpy as np

app = Flask(__name__)

con = sqlite3.connect('studybuddy.db', check_same_thread=False)
con.row_factory = sqlite3.Row
db = con.cursor()




def get_progress(course_id):
    lessons_all = db.execute("SELECT COUNT(status) FROM lessons WHERE course_id = ?", (course_id,)).fetchone()[0]

    if lessons_all == 0:
        return 0.5

    lessons_completed = db.execute("SELECT COUNT(status) FROM lessons WHERE course_id = ? AND status = 'completed'", (course_id,)).fetchone()[0]
    progress = np.round(lessons_completed / lessons_all * 100).astype(int)

    if progress > 100:
        progress = 100
    elif progress <= 0:
        progress = 0.5

    return progress




@app.route('/')
def index():
    skills = db.execute("SELECT * FROM skills")
    skills = skills.fetchall()

    return render_template('index.html', skills=skills)

@app.route("/skill<skill_id>")
def skill(skill_id=None):
    try:
        skill_name = db.execute("SELECT skill_name FROM skills WHERE skill_id = ?", (skill_id,))
        skill_name = skill_name.fetchone()["skill_name"]
    except Exception as e:
        print(f"Error retrieving skill_name for skill_id {skill_id}: {e}")
        return redirect(url_for("index"))

    courses = db.execute("SELECT * FROM courses WHERE skill_id = ?", (skill_id,))
    courses = courses.fetchall()

    # Create dict with progress values: KEY course_id, VALUE progress
    progress = {}
    for course in courses:
        progress[course["course_id"]] = get_progress(course["course_id"])

    return render_template("skill.html", skill_name=skill_name, skill_id=skill_id, courses=courses, progress=progress)

@app.route("/course<course_id>")
def course(course_id=None):
    try:
        course_name = db.execute("SELECT course_name FROM courses WHERE course_id = ?", (course_id,))
        course_name = course_name.fetchone()["course_name"]
        course_url = db.execute("SELECT url FROM courses WHERE course_id = ?", (course_id,)).fetchone()["url"]
    except Exception as e:
        print(f"Error retrieving course_name or course_url for course_id {course_id}: {e}")
        return redirect(url_for("index"))

    lessons = db.execute("SELECT * FROM lessons WHERE course_id = ?", (course_id,))
    lessons = lessons.fetchall()

    tasks = {}
    for lesson in lessons:
        lesson_id = lesson["lesson_id"]
        tasks[lesson_id] = db.execute("SELECT * FROM tasks WHERE lesson_id = ?", (lesson_id,)).fetchall()

    progress = get_progress(course_id)

    skill_id = db.execute("SELECT skill_id FROM courses WHERE course_id = ?", (course_id,)).fetchone()["skill_id"]

    return render_template("course.html", course_name=course_name, course_id=course_id, course_url=course_url, lessons=lessons, progress=progress, tasks=tasks, skill_id=skill_id)

@app.route("/add_item", methods=["POST"])
def add_item():
    try:
        item_type = request.form.get("item_type")
        item_name = request.form.get("item_name")
    except Exception as e:
        print(f"Error retrieving item_type or item_name: {e}")
        return redirect(url_for("index"))

    if item_type == "skill":
        db.execute("INSERT INTO skills (skill_name) VALUES (?)", (item_name,))

    elif item_type == "course":
        item_url = request.form.get("item_url")
        skill_id = request.form.get("top-relation")
        db.execute("INSERT INTO courses (course_name, skill_id, url) VALUES (?, ?, ?)", (item_name, skill_id, item_url))

    elif item_type == "lesson":
        course_id = request.form.get("top-relation")
        db.execute("INSERT INTO lessons (lesson_name, course_id) VALUES (?, ?)", (item_name, course_id))

    elif item_type == "task":
        lesson_id = request.form.get("top-relation")
        db.execute("INSERT INTO tasks (task_name, lesson_id) VALUES (?, ?)", (item_name, lesson_id))
    
    con.commit()

    return redirect(request.referrer or url_for("index"))

@app.route("/delete_item", methods=["POST"])
def delete_item(item_id=None, item_type=None):
    if not item_id or not item_type:
        try:
            item_id = request.form.get("item_id")
            item_type = request.form.get("item_type")
        except Exception as e:
            print(f"Error retrieving item_id or item_type: {e}")
            return redirect(url_for("index"))
        else:
            # Only redirect if function is triggered by a form submission
            # TODO: handle redirection based on original url
            delete_item(item_id, item_type)
            return redirect(request.referrer or url_for("index"))

    if item_type and item_id:
        if item_type == "skill":
            for course in db.execute("SELECT course_id FROM courses WHERE skill_id = ?", (item_id,)).fetchall():
                delete_item(course["course_id"], "course")
            db.execute("DELETE FROM skills WHERE skill_id = ?", (item_id,))

        elif item_type == "course":
            for lesson in db.execute("SELECT lesson_id FROM lessons WHERE course_id = ?", (item_id,)).fetchall():
                delete_item(lesson["lesson_id"], "lesson")
            db.execute("DELETE FROM courses WHERE course_id = ?", (item_id,))

        elif item_type == "lesson":
            for task in db.execute("SELECT task_id FROM tasks WHERE lesson_id = ?", (item_id,)).fetchall():
                delete_item(task["task_id"], "task")
            db.execute("DELETE FROM lessons WHERE lesson_id = ?", (item_id,))

        elif item_type == "task":
            db.execute("DELETE FROM tasks WHERE task_id = ?", (item_id,))
        
        con.commit()


@app.route("/update_status", methods=["POST"])
def update_status():
    lesson_id = request.form.get("lesson_id")
    task_id = request.form.get("task_id")
    toggle_status = request.form.get("toggle_status")

    if lesson_id and toggle_status:
        db.execute("UPDATE lessons SET status = ? WHERE lesson_id = ?", (toggle_status, lesson_id))
        con.commit()
    elif task_id and toggle_status:
        db.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (toggle_status, task_id))
        con.commit()
    
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    # For testing on this device
    app.run(debug=True)
    # For testing on local network
    # app.run(debug=True, host="192.168.0.197", port=8000)