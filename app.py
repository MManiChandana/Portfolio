import json
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "db.json"
UPLOAD_DIR = ROOT / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_UPLOADS = {"png", "jpg", "jpeg", "gif", "webp", "pdf", "mp4", "mov", "webm"}


DEFAULT_DATA = {
    "profile": {
        "name": "M Mani Chandana",
        "role": "Data Analyst | Data Scientist",
        "about": "Aspiring Data Analyst and Data Scientist passionate about transforming raw data into meaningful business insights using Python, SQL, Power BI, Statistics, and Machine Learning.",
        "hero_lines": "I build clean dashboards, practical analytics workflows, and machine learning experiments that turn raw data into decisions.",
        "resume": "#",
        "linkedin": "https://www.linkedin.com/in/mchandana10032003/",
        "github": "https://github.com/MManiChandana",
        "email": "mchandana10m2003@gmail.com",
        "hero_image": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1800&q=80",
        "profile_image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=900&q=80",
    },
    "skills": [
        {
            "name": "Python",
            "desc": "Python is my main language for data cleaning, automation, analysis, machine learning experiments, and backend logic.",
            "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        },
        {
            "name": "SQL",
            "desc": "SQL helps me query, model, and analyze structured data with joins, aggregations, CTEs, and window functions.",
            "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        },
        {
            "name": "Power BI",
            "desc": "Power BI lets me design interactive reports, KPI dashboards, and visual stories for business decisions.",
            "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/azuresqldatabase/azuresqldatabase-original.svg",
        },
        {
            "name": "Machine Learning",
            "desc": "I use machine learning to explore patterns, train predictive models, evaluate results, and improve decisions.",
            "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg",
        },
    ],
    "projects": [
        {
            "title": "Retail Sales Dashboard",
            "description": "Interactive analytics dashboard for sales KPIs, customer trends, and revenue insights.",
            "details": "This project analyzes retail sales performance across regions, categories, and time periods using clean KPI views and business-focused dashboards.",
            "tech": "SQL - Power BI - Analytics",
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
            "live_link": "#",
            "repo_link": "#",
        },
        {
            "title": "Netflix Data Analysis",
            "description": "Exploratory data analysis using Python, Pandas, and visualization libraries.",
            "details": "A complete EDA project focused on cleaning the Netflix dataset, finding trends, and presenting insights through useful visualizations.",
            "tech": "Python - Pandas - Visualization",
            "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            "live_link": "#",
            "repo_link": "#",
        },
    ],
    "certifications": [
        {
            "title": "Data Analytics Certification",
            "issuer": "Add Issuer",
            "date": "2026",
            "link": "#",
        }
    ],
    "messages": [],
}


def merge_defaults(data, defaults):
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict) and isinstance(data[key], dict):
            merge_defaults(data[key], value)
    return data


def normalize_data(data):
    data = merge_defaults(data, DEFAULT_DATA.copy())

    for skill in data.get("skills", []):
        if "desc" not in skill:
            skill["desc"] = skill.get("description", "")
        skill.setdefault("logo", "")

    for project in data.get("projects", []):
        project.setdefault("details", project.get("description", ""))
        project.setdefault("live_link", "#")
        project.setdefault("repo_link", "#")

    data.setdefault("certifications", [])
    data.setdefault("messages", [])
    return data


def load_data():
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return normalize_data(json.load(file))


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def uploaded_url(field_name):
    file = request.files.get(field_name)
    if not file or not file.filename:
        return ""

    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_UPLOADS:
        return ""

    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file.save(UPLOAD_DIR / filename)
    return url_for("static", filename=f"uploads/{filename}")


def update_from_form(target, fields):
    for field in fields:
        target[field] = request.form.get(field, "").strip()


@app.route("/")
def home():
    return render_template("index.html", data=load_data())


@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "profile":
            update_from_form(
                data["profile"],
                ["name", "role", "about", "hero_lines", "resume", "hero_image", "profile_image", "linkedin", "github", "email"],
            )
            for field in ("resume_file", "hero_image_file", "profile_image_file"):
                uploaded = uploaded_url(field)
                if uploaded:
                    data["profile"][field.replace("_file", "")] = uploaded

        elif action == "add_skill":
            data["skills"].append(
                {
                    "name": request.form.get("name", "").strip(),
                    "desc": request.form.get("desc", "").strip(),
                    "logo": request.form.get("logo", "").strip(),
                }
            )

        elif action == "update_skill":
            index = int(request.form.get("index", 0))
            update_from_form(data["skills"][index], ["name", "desc", "logo"])

        elif action == "add_project":
            image = uploaded_url("image_file") or request.form.get("image", "").strip()
            data["projects"].append(
                {
                    "title": request.form.get("title", "").strip(),
                    "description": request.form.get("description", "").strip(),
                    "details": request.form.get("details", "").strip(),
                    "tech": request.form.get("tech", "").strip(),
                    "image": image,
                    "live_link": request.form.get("live_link", "").strip(),
                    "repo_link": request.form.get("repo_link", "").strip(),
                }
            )

        elif action == "update_project":
            index = int(request.form.get("index", 0))
            update_from_form(data["projects"][index], ["title", "description", "details", "tech", "image", "live_link", "repo_link"])
            uploaded = uploaded_url("image_file")
            if uploaded:
                data["projects"][index]["image"] = uploaded

        elif action == "add_certification":
            data["certifications"].append(
                {
                    "title": request.form.get("title", "").strip(),
                    "issuer": request.form.get("issuer", "").strip(),
                    "date": request.form.get("date", "").strip(),
                    "link": request.form.get("link", "").strip(),
                }
            )

        elif action == "update_certification":
            index = int(request.form.get("index", 0))
            update_from_form(data["certifications"][index], ["title", "issuer", "date", "link"])

        save_data(data)
        return redirect(url_for("admin"))

    return render_template("admin.html", data=data, data_file=DATA_FILE.name)


@app.route("/delete/<section>/<int:index>", methods=["POST"])
def delete_item(section, index):
    data = load_data()
    if section in {"skills", "projects", "certifications", "messages"} and 0 <= index < len(data.get(section, [])):
        data[section].pop(index)
        save_data(data)
    return redirect(url_for("admin"))


@app.route("/contact", methods=["POST"])
def contact():
    data = load_data()
    message = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "message": request.form.get("message", "").strip(),
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    data.setdefault("messages", []).insert(0, message)
    save_data(data)

    subject = quote(f"Portfolio message from {message['name']}")
    body = quote(f"Name: {message['name']}\nEmail: {message['email']}\n\n{message['message']}")
    return redirect(f"mailto:{data['profile']['email']}?subject={subject}&body={body}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
