import json
import os
import secrets
import smtplib
import uuid
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import quote
import urllib.request
import urllib.parse

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "db.json"
UPLOAD_DIR = ROOT / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
INTRO_DIR = UPLOAD_DIR / "intro"
INTRO_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_UPLOADS = {"png", "jpg", "jpeg", "gif", "webp", "pdf", "mp4", "mov", "webm"}
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "mchandana10m2003@gmail.com").lower()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Manu@1428")


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
            "image": "",
        }
    ],
    "virtual_projects": [],
    "messages": [],
    "settings": {},
    "intro_images": [],
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
        # normalize logo field: allow either a single string or a list of strings
        logo_val = skill.get("logo", "")
        if isinstance(logo_val, list):
            skill["logo"] = logo_val
        elif logo_val:
            skill["logo"] = [logo_val]
        else:
            skill["logo"] = []

    for project in data.get("projects", []):
        project.setdefault("details", project.get("description", ""))
        project.setdefault("live_link", "#")
        project.setdefault("repo_link", "#")

    data.setdefault("certifications", [])
    data.setdefault("virtual_projects", [])
    for virtual_project in data.get("virtual_projects", []):
        virtual_project.setdefault("company", virtual_project.get("issuer", ""))
        virtual_project.setdefault("description", virtual_project.get("details", ""))
        virtual_project.setdefault("details", virtual_project.get("description", ""))
        virtual_project.setdefault("skills", "")
        virtual_project.setdefault("image", "")
        virtual_project.setdefault("link", "")
    data.setdefault("messages", [])
    data.setdefault("settings", {})
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
        file.flush()
        os.fsync(file.fileno())


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


def uploaded_intro_url(field_name):
    file = request.files.get(field_name)
    if not file or not file.filename:
        return ""

    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_UPLOADS:
        return ""

    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file.save(INTRO_DIR / filename)
    return url_for("static", filename=f"uploads/intro/{filename}")


def update_from_form(target, fields):
    for field in fields:
        target[field] = request.form.get(field, "").strip()


def verify_admin_password(data, password):
    password_hash = data.get("settings", {}).get("admin_password_hash")
    if password_hash:
        return check_password_hash(password_hash, password)
    return password == ADMIN_PASSWORD


def set_admin_password(data, password):
    data.setdefault("settings", {})["admin_password_hash"] = generate_password_hash(password)
    data["settings"].pop("reset_token", None)
    data["settings"].pop("reset_expires", None)


def create_reset_token(data):
    token = secrets.token_urlsafe(32)
    data.setdefault("settings", {})["reset_token"] = token
    data["settings"]["reset_expires"] = (datetime.utcnow() + timedelta(minutes=30)).isoformat()
    return token


def reset_token_is_valid(data, token):
    settings = data.get("settings", {})
    expires = settings.get("reset_expires", "")
    if not token or token != settings.get("reset_token"):
        return False

    try:
        return datetime.utcnow() <= datetime.fromisoformat(expires)
    except ValueError:
        return False


def send_password_reset_email(reset_link):
    mail_server = os.environ.get("MAIL_SERVER")
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")
    if not mail_server or not mail_username or not mail_password:
        return False

    message = EmailMessage()
    message["Subject"] = "Portfolio admin password reset"
    message["From"] = os.environ.get("MAIL_FROM", mail_username)
    message["To"] = ADMIN_EMAIL
    message.set_content(
        "Use this link to reset your portfolio admin password. "
        "The link expires in 30 minutes.\n\n"
        f"{reset_link}"
    )

    mail_port = int(os.environ.get("MAIL_PORT", "587"))
    use_tls = os.environ.get("MAIL_USE_TLS", "true").lower() != "false"

    with smtplib.SMTP(mail_server, mail_port) as smtp:
        if use_tls:
            smtp.starttls()
        smtp.login(mail_username, mail_password)
        smtp.send_message(message)

    return True


@app.route("/")
def home():
    data = load_data()
    # Prefer intro image list stored in data (admin-managed), otherwise read folder
    intro_images = []
    for image in data.get("intro_images", []) or []:
        if image.startswith("/static/uploads/"):
            image_path = UPLOAD_DIR / urllib.parse.unquote(image.split("/static/uploads/", 1)[1])
            if image_path.exists():
                intro_images.append(image)
        else:
            intro_images.append(image)

    if not intro_images:
        try:
            for p in sorted(INTRO_DIR.iterdir()):
                if p.is_file():
                    intro_images.append(url_for("static", filename=f"uploads/intro/{p.name}"))
                if len(intro_images) >= 8:
                    break
        except Exception:
            intro_images = []

    return render_template("index.html", data=data, intro_images=intro_images)


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    data = load_data()
    error = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if email == ADMIN_EMAIL and verify_admin_password(data, password):
            session["admin_email"] = email
            return redirect(url_for("admin"))
        error = "Enter the owner email and password to continue."

    return render_template("admin_login.html", data=data, error=error)


@app.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    data = load_data()
    notice = "If this is the owner email, a reset link will be sent."
    email = request.form.get("email", "").strip().lower()

    if email == ADMIN_EMAIL:
        token = create_reset_token(data)
        save_data(data)
        reset_link = url_for("reset_password", token=token, _external=True)
        try:
            if not send_password_reset_email(reset_link):
                notice = "Email is not configured yet. Add SMTP settings in Render to receive reset links."
        except OSError:
            notice = "Email could not be sent. Please check SMTP settings in Render."
        except smtplib.SMTPException:
            notice = "Email could not be sent. Please check SMTP username and app password."

    return render_template("admin_login.html", data=data, notice=notice, error="")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    data = load_data()
    if not reset_token_is_valid(data, token):
        return render_template("reset_password.html", data=data, token="", error="This reset link is invalid or expired.", notice="")

    error = ""
    notice = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        if len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            set_admin_password(data, password)
            save_data(data)
            session["admin_email"] = ADMIN_EMAIL
            return redirect(url_for("admin"))

    return render_template("reset_password.html", data=data, token=token, error=error, notice=notice)


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_email", None)
    return redirect(url_for("home"))


@app.route("/admin-change-password", methods=["GET", "POST"])
def admin_change_password():
    if session.get("admin_email") != ADMIN_EMAIL:
        return redirect(url_for("admin_login"))

    data = load_data()
    error = ""
    notice = ""

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not verify_admin_password(data, current_password):
            error = "Current password is incorrect."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            set_admin_password(data, password)
            save_data(data)
            notice = "Password updated successfully."

    return render_template("change_password.html", data=data, error=error, notice=notice)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("admin_email") != ADMIN_EMAIL:
        return redirect(url_for("admin_login"))

    data = load_data()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "profile":
            update_from_form(
                data["profile"],
                ["name", "role", "about", "hero_lines", "resume", "hero_image", "profile_image", "profile_video", "profile_audio", "linkedin", "github", "email"],
            )
            for field in ("resume_file", "hero_image_file", "profile_image_file", "profile_video_file", "profile_audio_file"):
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
            image = uploaded_url("image_file") or request.form.get("image", "").strip()
            data["certifications"].append(
                {
                    "title": request.form.get("title", "").strip(),
                    "issuer": request.form.get("issuer", "").strip(),
                    "date": request.form.get("date", "").strip(),
                    "link": request.form.get("link", "").strip(),
                    "image": image,
                }
            )

        elif action == "add_virtual_project":
            image = uploaded_url("image_file") or request.form.get("image", "").strip()
            data.setdefault("virtual_projects", []).append(
                {
                    "title": request.form.get("title", "").strip(),
                    "company": request.form.get("company", "").strip(),
                    "description": request.form.get("description", "").strip(),
                    "details": request.form.get("details", "").strip(),
                    "skills": request.form.get("skills", "").strip(),
                    "image": image,
                    "link": request.form.get("link", "").strip(),
                }
            )

        elif action == "add_intro_image":
            added = []
            # handle multiple uploaded files input name intro_image_files
            files = request.files.getlist("intro_image_files")
            for f in files:
                if f and f.filename:
                    extension = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
                    if extension in ALLOWED_UPLOADS:
                        filename = f"{uuid.uuid4().hex}_{secure_filename(f.filename)}"
                        f.save(INTRO_DIR / filename)
                        added.append(url_for("static", filename=f"uploads/intro/{filename}"))

            # fallback single file field name (backwards compatibility)
            single = uploaded_intro_url("intro_image_file")
            if single:
                added.append(single)

            # also allow a pasted URL
            url_field = request.form.get("intro_image", "").strip()
            if url_field:
                # if it's a remote URL, download and save it locally for permanence
                if url_field.lower().startswith("http"):
                    try:
                        parsed = urllib.parse.urlparse(url_field)
                        basename = Path(parsed.path).name
                        ext = basename.rsplit('.', 1)[-1].lower() if '.' in basename else ''
                        if ext not in ALLOWED_UPLOADS:
                            # try to detect from content-type
                            resp = urllib.request.urlopen(url_field)
                            ctype = resp.headers.get_content_type()
                            mapping = {'image/jpeg':'jpg','image/png':'png','image/gif':'gif','image/webp':'webp'}
                            ext = mapping.get(ctype, '')
                            data_bytes = resp.read()
                        else:
                            data_bytes = urllib.request.urlopen(url_field).read()

                        if ext and ext in ALLOWED_UPLOADS:
                            filename = f"{uuid.uuid4().hex}_{secure_filename(basename)}"
                            with open(INTRO_DIR / filename, 'wb') as out_f:
                                out_f.write(data_bytes)
                            added.append(url_for("static", filename=f"uploads/intro/{filename}"))
                        else:
                            # fallback: store original URL (not downloaded)
                            added.append(url_field)
                    except Exception:
                        # if download fails, still store URL
                        added.append(url_field)
                else:
                    added.append(url_field)

            if added:
                data.setdefault("intro_images", []).extend(added)

        elif action == "remove_intro":
            index = int(request.form.get("index", 0))
            imgs = data.get("intro_images", [])
            if 0 <= index < len(imgs):
                removed = imgs.pop(index)
                # if removed points to a local uploads/intro file, delete it from disk
                try:
                    if isinstance(removed, str) and 'uploads/intro/' in removed:
                        fname = removed.split('uploads/intro/')[-1]
                        fpath = INTRO_DIR / fname
                        if fpath.exists():
                            fpath.unlink()
                except Exception:
                    pass
                data["intro_images"] = imgs

        elif action == "update_certification":
            index = int(request.form.get("index", 0))
            update_from_form(data["certifications"][index], ["title", "issuer", "date", "link", "image"])
            uploaded = uploaded_url("image_file")
            if uploaded:
                data["certifications"][index]["image"] = uploaded

        elif action == "update_virtual_project":
            index = int(request.form.get("index", 0))
            update_from_form(data["virtual_projects"][index], ["title", "company", "description", "details", "skills", "image", "link"])
            uploaded = uploaded_url("image_file")
            if uploaded:
                data["virtual_projects"][index]["image"] = uploaded

        save_data(data)
        return redirect(url_for("admin"))

    return render_template("admin.html", data=data, data_file=DATA_FILE.name)


@app.route("/delete/<section>/<int:index>", methods=["POST"])
def delete_item(section, index):
    if session.get("admin_email") != ADMIN_EMAIL:
        return redirect(url_for("admin_login"))

    data = load_data()
    if section in {"skills", "projects", "certifications", "virtual_projects", "messages"} and 0 <= index < len(data.get(section, [])):
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
