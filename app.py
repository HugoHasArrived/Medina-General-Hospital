from flask import Flask, request, redirect, url_for, session, flash, render_template_string, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import sqlite3
import os
import secrets
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "clinic.db"

app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
if os.environ.get("RENDER"):
    app.config["SESSION_COOKIE_SECURE"] = True


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    db = get_db()

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff',
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS assistance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            concern TEXT NOT NULL,
            urgency TEXT NOT NULL DEFAULT 'Normal',
            preferred_language TEXT NOT NULL DEFAULT 'English',
            status TEXT NOT NULL DEFAULT 'New',
            staff_note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )

    existing = db.execute(
        "SELECT id FROM staff WHERE username = ?",
        ("admin",),
    ).fetchone()

    if existing is None:
        default_password = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")
        db.execute(
            """
            INSERT INTO staff
            (username, password_hash, role, active, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "admin",
                generate_password_hash(default_password),
                "admin",
                1,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )

    db.commit()
    db.close()


initialize_database()


def staff_required(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if not session.get("staff_logged_in"):
            return redirect(url_for("staff_login"))
        return function(*args, **kwargs)

    return wrapped


def clean_text(value, limit=1000):
    value = (value or "").strip()
    return value[:limit]


def page(title, content, staff=False):
    logged_in = session.get("staff_logged_in", False)

    return render_template_string(
        """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} | Dr. Bebie Tagupa</title>
<meta name="description" content="Dr. Bebie Queen Lucelle R. Tagupa - Licensed Physician and Psychiatrist">

<style>
:root{
    --purple:#7c3aed;
    --purple-dark:#5b21b6;
    --purple-light:#a78bfa;
    --bg:#faf8ff;
    --bg2:#f1ebff;
    --card:#ffffff;
    --text:#21152d;
    --muted:#6f6479;
    --border:rgba(124,58,237,.15);
    --green:#15803d;
    --yellow:#a16207;
    --red:#b91c1c;
}

body.dark{
    --bg:#100917;
    --bg2:#1b1025;
    --card:#1e1429;
    --text:#f8f3ff;
    --muted:#c8bdd4;
    --border:rgba(167,139,250,.20);
}

*{box-sizing:border-box;margin:0;padding:0}

html{scroll-behavior:smooth}

body{
    font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    background:
        radial-gradient(circle at 8% 4%,rgba(124,58,237,.11),transparent 28%),
        radial-gradient(circle at 92% 18%,rgba(167,139,250,.10),transparent 28%),
        var(--bg);
    color:var(--text);
    line-height:1.6;
    transition:.25s;
}

a{text-decoration:none;color:inherit}

button,input,select,textarea{font:inherit}

.container{width:min(1120px,92%);margin:auto}

header{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    z-index:1000;
    background:rgba(250,248,255,.86);
    backdrop-filter:blur(18px);
    border-bottom:1px solid var(--border);
}

body.dark header{background:rgba(16,9,23,.86)}

nav{
    min-height:76px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
}

.logo{
    width:44px;
    height:44px;
    display:grid;
    place-items:center;
    border-radius:14px;
    color:#fff;
    background:linear-gradient(135deg,var(--purple),var(--purple-dark));
    font-size:21px;
}

.brand small{
    display:block;
    color:var(--purple);
    font-size:10px;
    font-weight:900;
    letter-spacing:1.2px;
    text-transform:uppercase;
}

.brand strong{
    display:block;
    font-size:15px;
}

.nav-links{
    display:flex;
    gap:23px;
}

.nav-links a{
    color:var(--muted);
    font-size:14px;
    font-weight:700;
}

.nav-links a:hover{color:var(--purple)}

.actions{
    display:flex;
    gap:8px;
    align-items:center;
}

.language,
.theme{
    height:40px;
    border:1px solid var(--border);
    border-radius:12px;
    background:var(--card);
    color:var(--text);
}

.language{
    padding:0 10px;
    cursor:pointer;
}

.theme{
    width:40px;
    cursor:pointer;
}

main{padding-top:76px}

section{padding:90px 0}

.hero{
    padding:85px 0;
}

.hero-grid{
    display:grid;
    grid-template-columns:1.05fr .95fr;
    gap:60px;
    align-items:center;
}

.pill{
    display:inline-flex;
    padding:8px 13px;
    margin-bottom:18px;
    border-radius:999px;
    color:var(--purple-dark);
    background:var(--bg2);
    font-size:11px;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:1px;
}

body.dark .pill{color:#dfd2ff}

h1{
    font-size:clamp(42px,6vw,70px);
    line-height:1.03;
    letter-spacing:-3px;
    margin-bottom:20px;
}

.purple{color:var(--purple)}

.hero-text{
    max-width:640px;
    color:var(--muted);
    font-size:18px;
    line-height:1.8;
    margin-bottom:28px;
}

.buttons{
    display:flex;
    flex-wrap:wrap;
    gap:12px;
}

.btn{
    min-height:50px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    padding:0 20px;
    border-radius:14px;
    font-size:14px;
    font-weight:800;
    cursor:pointer;
    border:0;
}

.btn-primary{
    color:#fff;
    background:linear-gradient(135deg,var(--purple),var(--purple-dark));
    box-shadow:0 14px 30px rgba(124,58,237,.22);
}

.btn-secondary{
    color:var(--text);
    background:var(--card);
    border:1px solid var(--border);
}

.photo-wrap{
    display:flex;
    justify-content:center;
    position:relative;
}

.photo-card{
    position:relative;
    width:min(420px,100%);
    padding:11px;
    border-radius:31px;
    background:linear-gradient(145deg,#fff,#eee7ff);
    box-shadow:0 20px 55px rgba(81,45,120,.14);
    transform:rotate(1deg);
}

body.dark .photo-card{
    background:linear-gradient(145deg,#3a274d,#1c1226);
}

.doctor-photo{
    width:100%;
    aspect-ratio:4/5;
    object-fit:cover;
    display:block;
    border-radius:23px;
    background:var(--bg2);
}

.badge{
    position:absolute;
    bottom:25px;
    left:-22px;
    padding:14px 17px;
    border-radius:16px;
    background:var(--card);
    border:1px solid var(--border);
    box-shadow:0 18px 50px rgba(74,38,110,.14);
}

.badge strong{display:block;font-size:13px}
.badge span{font-size:11px;color:var(--muted)}

.quick-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
}

.quick-card{
    padding:24px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:20px;
    box-shadow:0 18px 50px rgba(74,38,110,.08);
}

.quick-icon{font-size:25px;margin-bottom:9px}
.quick-card h3{font-size:16px;margin-bottom:4px}
.quick-card p{font-size:13px;color:var(--muted)}

.section-alt{background:var(--bg2)}

.heading{
    max-width:720px;
    text-align:center;
    margin:0 auto 45px;
}

.kicker{
    color:var(--purple);
    font-size:11px;
    font-weight:900;
    letter-spacing:2px;
    text-transform:uppercase;
    margin-bottom:9px;
}

.heading h2{
    font-size:clamp(32px,5vw,48px);
    line-height:1.1;
    letter-spacing:-1.8px;
    margin-bottom:12px;
}

.heading p{color:var(--muted)}

.about-grid{
    display:grid;
    grid-template-columns:.78fr 1.22fr;
    gap:56px;
    align-items:center;
}

.quote{
    padding:34px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:27px;
    box-shadow:0 18px 50px rgba(74,38,110,.10);
    font-size:28px;
    font-weight:850;
    line-height:1.3;
}

.quote span{color:var(--purple)}

.about-text h2{
    font-size:41px;
    letter-spacing:-1.5px;
    margin-bottom:17px;
}

.about-text p{
    color:var(--muted);
    margin-bottom:14px;
}

.services{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
}

.service{
    padding:29px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:23px;
    box-shadow:0 18px 50px rgba(74,38,110,.08);
}

.service-icon{
    width:53px;
    height:53px;
    display:grid;
    place-items:center;
    border-radius:15px;
    background:var(--bg2);
    font-size:24px;
    margin-bottom:17px;
}

.service h3{font-size:18px;margin-bottom:8px}
.service p{color:var(--muted);font-size:14px}

.clinic-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:20px;
}

.clinic{
    padding:31px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:23px;
    box-shadow:0 18px 50px rgba(74,38,110,.08);
}

.clinic h3{font-size:21px;margin-bottom:14px}

.row{
    display:flex;
    gap:13px;
    align-items:flex-start;
    padding:15px 0;
    border-bottom:1px solid var(--border);
}

.row:last-child{border-bottom:0}

.row-icon{
    width:42px;
    height:42px;
    flex:none;
    display:grid;
    place-items:center;
    border-radius:12px;
    background:var(--bg2);
}

.row strong{display:block;font-size:14px}
.row span{color:var(--muted);font-size:14px}

.assistance-box{
    position:relative;
    overflow:hidden;
    padding:45px;
    border-radius:30px;
    color:white;
    background:linear-gradient(135deg,#4c1d95,#7c3aed);
    box-shadow:0 25px 65px rgba(91,33,182,.22);
}

.assistance-box h2{
    font-size:clamp(30px,5vw,45px);
    letter-spacing:-1.5px;
    line-height:1.1;
    margin-bottom:12px;
}

.assistance-box p{
    max-width:690px;
    color:rgba(255,255,255,.80);
    margin-bottom:24px;
}

.assistance-form{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
}

.form-full{grid-column:1/-1}

.assistance-form label{
    display:block;
    font-size:13px;
    font-weight:800;
    margin-bottom:5px;
}

.assistance-form input,
.assistance-form select,
.assistance-form textarea{
    width:100%;
    padding:12px 13px;
    border:1px solid rgba(255,255,255,.22);
    border-radius:12px;
    outline:none;
    background:rgba(255,255,255,.12);
    color:white;
}

.assistance-form option{
    color:#21152d;
}

.assistance-form textarea{
    min-height:110px;
    resize:vertical;
}

.assistance-form input::placeholder,
.assistance-form textarea::placeholder{
    color:rgba(255,255,255,.64);
}

.form-note{
    margin-top:12px;
    color:rgba(255,255,255,.72);
    font-size:12px;
}

.flash{
    width:min(1120px,92%);
    margin:18px auto 0;
    padding:14px 16px;
    border-radius:12px;
    border-left:5px solid var(--purple);
    background:var(--card);
    border:1px solid var(--border);
}

.flash.success{border-left-color:var(--green)}
.flash.warning{border-left-color:var(--yellow)}
.flash.danger{border-left-color:var(--red)}

footer{
    padding:35px 0;
    background:var(--bg2);
    border-top:1px solid var(--border);
}

.footer-row{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
}

.footer-row span{color:var(--muted);font-size:12px}

/* STAFF */

.staff-header{
    padding:70px 0 30px;
}

.staff-title{
    display:flex;
    align-items:flex-end;
    justify-content:space-between;
    gap:20px;
}

.staff-title h1{
    font-size:clamp(34px,5vw,55px);
    letter-spacing:-2px;
    margin-bottom:7px;
}

.staff-title p{color:var(--muted)}

.staff-actions{
    display:flex;
    gap:9px;
    flex-wrap:wrap;
}

.stats{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin:25px 0;
}

.stat{
    padding:22px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:19px;
}

.stat-number{
    display:block;
    color:var(--purple);
    font-size:39px;
    font-weight:900;
}

.stat-label{
    color:var(--muted);
    font-size:13px;
}

.requests{
    display:grid;
    gap:15px;
}

.request{
    padding:23px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:20px;
    box-shadow:0 12px 35px rgba(74,38,110,.07);
}

.request.new{
    border-color:rgba(124,58,237,.38);
    box-shadow:
        0 0 0 2px rgba(124,58,237,.05),
        0 14px 40px rgba(124,58,237,.10);
}

.request-top{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:15px;
}

.request-name{
    font-size:19px;
    font-weight:900;
}

.request-time{
    color:var(--muted);
    font-size:12px;
}

.badges{
    display:flex;
    gap:7px;
    flex-wrap:wrap;
    margin:11px 0;
}

.badge-status{
    display:inline-flex;
    padding:5px 10px;
    border-radius:999px;
    font-size:11px;
    font-weight:900;
    background:var(--bg2);
    color:var(--purple);
}

.badge-urgent{
    background:#fee2e2;
    color:#991b1b;
}

body.dark .badge-urgent{
    background:#451a1a;
    color:#fecaca;
}

.request-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin:16px 0;
}

.request-field{
    padding:13px;
    border-radius:13px;
    background:var(--bg2);
}

.request-field strong{
    display:block;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:.7px;
    color:var(--purple);
    margin-bottom:4px;
}

.request-field span{
    font-size:13px;
}

.request-actions{
    display:flex;
    gap:8px;
    flex-wrap:wrap;
    margin-top:14px;
}

.request-actions form{
    margin:0;
}

.empty{
    padding:55px 25px;
    text-align:center;
    color:var(--muted);
    background:var(--card);
    border:1px solid var(--border);
    border-radius:20px;
}

.login-card{
    max-width:500px;
    margin:70px auto;
    padding:32px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:24px;
    box-shadow:0 18px 50px rgba(74,38,110,.10);
}

.login-card h1{
    font-size:35px;
    letter-spacing:-1.5px;
}

.field{margin-bottom:15px}

.field label{
    display:block;
    margin-bottom:5px;
    font-size:13px;
    font-weight:800;
}

.field input,
.field textarea,
.field select{
    width:100%;
    padding:12px 13px;
    border:1px solid var(--border);
    border-radius:11px;
    background:var(--card);
    color:var(--text);
    outline:none;
}

.note{
    color:var(--muted);
    font-size:12px;
    margin-top:10px;
}

/* RESPONSIVE */

@media(max-width:900px){
    .nav-links{display:none}
    .hero-grid,
    .about-grid,
    .clinic-grid{
        grid-template-columns:1fr;
    }

    .quick-grid,
    .services,
    .stats{
        grid-template-columns:1fr;
    }

    .photo-area{order:-1}
    .assistance-form{grid-template-columns:1fr}
    .form-full{grid-column:auto}
    .request-grid{grid-template-columns:1fr}
    .staff-title{flex-direction:column;align-items:flex-start}
    .footer-row{flex-direction:column;text-align:center}
}

@media(max-width:560px){
    .brand small,.brand strong{display:none}
    section{padding:72px 0}
    .hero{padding:65px 0}
    h1{font-size:43px}
    .hero-text{font-size:16px}
    .buttons{flex-direction:column}
    .btn{width:100%}
    .assistance-box{padding:30px 22px}
    .badge{left:7px}
}
</style>
</head>

<body>

<header>
<div class="container">
<nav>

<a class="brand" href="{{ url_for('home') }}">
    <div class="logo">♡</div>
    <div>
        <small>Psychiatry & Mental Wellness</small>
        <strong>Dr. Bebie Tagupa</strong>
    </div>
</a>

<div class="nav-links">
    {% if staff %}
        <a href="{{ url_for('staff_dashboard') }}">Staff Dashboard</a>
        <a href="{{ url_for('home') }}">Public Site</a>
        <a href="{{ url_for('logout') }}">Log Out</a>
    {% else %}
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#services">Services</a>
        <a href="#clinic">Clinic</a>
        <a href="#assistance">Assistance</a>
        <a href="{{ url_for('staff_login') }}">Staff</a>
    {% endif %}
</div>

<div class="actions">
    <select class="language" id="language" aria-label="Language" onchange="changeLanguage()">
        <option value="en">English</option>
        <option value="fil">Filipino</option>
        <option value="ceb">Visaya</option>
    </select>

    <button class="theme" type="button" id="themeButton" onclick="toggleTheme()">🌙</button>
</div>

</nav>
</div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}

<main class="container">
{{ content|safe }}
</main>

<footer>
<div class="container">
<div class="footer-row">
    <strong>Dr. Bebie Queen Lucelle R. Tagupa</strong>
    <span>Licensed Physician • Psychiatrist • © 2026</span>
</div>
</div>
</footer>

<script>
function toggleTheme(){
    document.body.classList.toggle("dark");
    const dark = document.body.classList.contains("dark");
    localStorage.setItem("doctorTheme", dark ? "dark" : "light");
    document.getElementById("themeButton").textContent = dark ? "☀️" : "🌙";
}

function changeLanguage(){
    const language = document.getElementById("language").value;
    localStorage.setItem("doctorLanguage", language);

    document.querySelectorAll(".language-content").forEach(function(el){
        el.style.display = "none";
    });

    document.querySelectorAll('[data-language="' + language + '"]').forEach(function(el){
        el.style.display = "block";
    });
}

(function(){
    const savedTheme = localStorage.getItem("doctorTheme");
    if(savedTheme === "dark"){
        document.body.classList.add("dark");
    }
    document.getElementById("themeButton").textContent =
        document.body.classList.contains("dark") ? "☀️" : "🌙";

    const savedLanguage = localStorage.getItem("doctorLanguage") || "en";
    document.getElementById("language").value = savedLanguage;
    changeLanguage();
})();

{% if staff %}
let lastKnownNewCount = {{ new_count }};

setInterval(function(){
    fetch("{{ url_for('staff_status') }}", {
        headers: {"Accept":"application/json"}
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        const badge = document.getElementById("liveNewCount");
        if(badge){
            badge.textContent = data.new_count;
        }

        if(data.new_count > lastKnownNewCount){
            location.reload();
        }

        lastKnownNewCount = data.new_count;
    })
    .catch(function(){});
}, 10000);
{% endif %}
</script>

</body>
</html>
        """,
        title=title,
        content=content,
        staff=staff,
        new_count=get_new_count(),
    )


def get_new_count():
    db = get_db()
    count = db.execute(
        "SELECT COUNT(*) FROM assistance_requests WHERE status = 'New'"
    ).fetchone()[0]
    db.close()
    return count


@app.route("/")
def home():
    content = """
<section class="hero" id="home">
    <div class="hero-grid">
        <div>
            <div class="pill">✦ Licensed Physician & Psychiatrist</div>

            <div class="language-content" data-language="en">
                <h1>Your mind deserves <span class="purple">care.</span></h1>
                <p class="hero-text">
                    Compassionate, patient-centered psychiatric care focused
                    on helping you understand your mental well-being, find
                    support, and move toward a healthier and more fulfilling life.
                </p>
                <div class="buttons">
                    <a class="btn btn-primary" href="#assistance">💜 I Need Assistance</a>
                    <a class="btn btn-secondary" href="#about">Meet Dr. Tagupa →</a>
                </div>
            </div>

            <div class="language-content" data-language="fil" style="display:none">
                <h1>Ang iyong isip ay <span class="purple">mahalaga.</span></h1>
                <p class="hero-text">
                    Maalagang psychiatric care na nakatuon sa bawat pasyente.
                    Layunin naming makatulong sa iyong mental well-being at
                    pangkalahatang kalidad ng buhay.
                </p>
                <div class="buttons">
                    <a class="btn btn-primary" href="#assistance">💜 Kailangan Ko ng Tulong</a>
                    <a class="btn btn-secondary" href="#about">Kilalanin si Dr. Tagupa →</a>
                </div>
            </div>

            <div class="language-content" data-language="ceb" style="display:none">
                <h1>Importante ang imong <span class="purple">hunahuna.</span></h1>
                <p class="hero-text">
                    Mainiton ug maloloy-on nga psychiatric care nga
                    nakasentro sa panginahanglan sa matag pasyente.
                </p>
                <div class="buttons">
                    <a class="btn btn-primary" href="#assistance">💜 Nanginahanglan Ko og Tabang</a>
                    <a class="btn btn-secondary" href="#about">Ilaila si Dr. Tagupa →</a>
                </div>
            </div>
        </div>

        <div class="photo-wrap">
            <div class="photo-card">
                <img
                    class="doctor-photo"
                    src="/static/image0%20%282%29.jpeg"
                    alt="Dr. Bebie Queen Lucelle R. Tagupa"
                >
                <div class="badge">
                    <strong>Dr. Bebie Queen Lucelle R. Tagupa</strong>
                    <span>Licensed Physician • Psychiatrist</span>
                </div>
            </div>
        </div>
    </div>
</section>

<section>
    <div class="quick-grid">
        <div class="quick-card">
            <div class="quick-icon">🩺</div>
            <h3>Licensed Physician</h3>
            <p>Medical doctor committed to compassionate, patient-centered care.</p>
        </div>

        <div class="quick-card">
            <div class="quick-icon">🧠</div>
            <h3>Psychiatry</h3>
            <p>Psychiatric evaluation and treatment for a wide range of conditions.</p>
        </div>

        <div class="quick-card">
            <div class="quick-icon">💜</div>
            <h3>Patient-Centered</h3>
            <p>Your story, concerns, and well-being are at the heart of every consultation.</p>
        </div>
    </div>
</section>

<section class="section-alt" id="about">
    <div class="heading">
        <div class="kicker">About the Doctor</div>
        <h2>Compassion backed by training.</h2>
        <p>Professional medical and psychiatric training with a patient-centered approach.</p>
    </div>

    <div class="about-grid">
        <div class="quote">
            “Mental health care begins with <span>being heard.</span>”
        </div>

        <div class="about-text language-content" data-language="en">
            <h2>Meet Dr. Tagupa</h2>
            <p>
                Dr. Bebie Queen Lucelle R. Tagupa is a licensed physician and
                psychiatrist dedicated to providing compassionate, patient-centered
                mental health care.
            </p>
            <p>
                She earned her Bachelor’s degree in Medical Technology from
                Velez College and is also a licensed Medical Technologist.
            </p>
            <p>
                She proceeded to study Medicine at Xavier University – Ateneo de Cagayan.
            </p>
            <p>
                She completed her post-graduate internship at Davao Doctors Hospital
                and finished her residency training in Psychiatry at the Southern
                Philippines Medical Center – Institute of Psychiatry and Behavioral Medicine.
            </p>
            <p>
                During her final year of training, she served as Chief Resident and
                was awarded Most Outstanding Resident in Psychiatry during her graduation.
            </p>
        </div>

        <div class="about-text language-content" data-language="fil" style="display:none">
            <h2>Kilalanin si Dr. Tagupa</h2>
            <p>
                Si Dr. Bebie Queen Lucelle R. Tagupa ay isang licensed physician
                at psychiatrist na nakatuon sa mahabagin at patient-centered na
                pangangalaga sa mental health.
            </p>
            <p>
                Natapos niya ang Bachelor’s degree sa Medical Technology sa Velez College
                at isa rin siyang licensed Medical Technologist.
            </p>
            <p>
                Nagpatuloy siya sa Medicine sa Xavier University – Ateneo de Cagayan.
            </p>
            <p>
                Nakumpleto niya ang post-graduate internship sa Davao Doctors Hospital
                at residency training sa Psychiatry sa Southern Philippines Medical Center –
                Institute of Psychiatry and Behavioral Medicine.
            </p>
            <p>
                Sa kanyang huling taon ng training, nagsilbi siya bilang Chief Resident
                at ginawaran bilang Most Outstanding Resident in Psychiatry.
            </p>
        </div>

        <div class="about-text language-content" data-language="ceb" style="display:none">
            <h2>Ilaila si Dr. Tagupa</h2>
            <p>
                Si Dr. Bebie Queen Lucelle R. Tagupa usa ka licensed physician
                ug psychiatrist nga naghatag og maloloy-on ug patient-centered
                nga mental health care.
            </p>
            <p>
                Nakakuha siya sa iyang Bachelor’s degree sa Medical Technology
                gikan sa Velez College ug usa usab siya ka licensed Medical Technologist.
            </p>
            <p>
                Nagpadayon siya sa pagtuon og Medicine sa Xavier University – Ateneo de Cagayan.
            </p>
            <p>
                Nakompleto niya ang post-graduate internship sa Davao Doctors Hospital
                ug residency training sa Psychiatry sa Southern Philippines Medical Center –
                Institute of Psychiatry and Behavioral Medicine.
            </p>
            <p>
                Sa iyang katapusang tuig sa training, nagsilbi siya isip Chief Resident
                ug nadawat ang award nga Most Outstanding Resident in Psychiatry.
            </p>
        </div>
    </div>
</section>

<section id="services">
    <div class="heading">
        <div class="kicker">Mental Health Care</div>
        <h2>Care that starts with you.</h2>
        <p>Support for understanding your mental well-being and moving forward.</p>
    </div>

    <div class="services">
        <div class="service">
            <div class="service-icon">🧠</div>
            <h3>Psychiatric Evaluation</h3>
            <p>Comprehensive assessment to better understand mental health concerns.</p>
        </div>

        <div class="service">
            <div class="service-icon">💬</div>
            <h3>Mental Health Consultation</h3>
            <p>A respectful space to discuss concerns, emotions, thoughts, and behavior.</p>
        </div>

        <div class="service">
            <div class="service-icon">🌱</div>
            <h3>Treatment & Follow-Up</h3>
            <p>Patient-centered treatment and follow-up based on individual needs.</p>
        </div>
    </div>
</section>

<section class="section-alt" id="clinic">
    <div class="heading">
        <div class="kicker">Clinic Information</div>
        <h2>Visit the clinic.</h2>
        <p>Find the location and consultation schedule below.</p>
    </div>

    <div class="clinic-grid">
        <div class="clinic">
            <h3>📍 Clinic</h3>

            <div class="row">
                <div class="row-icon">🏥</div>
                <div>
                    <strong>Hospital</strong>
                    <span>Medina General Hospital</span>
                </div>
            </div>

            <div class="row">
                <div class="row-icon">🚪</div>
                <div>
                    <strong>Location</strong>
                    <span>OPD Door 2</span>
                </div>
            </div>
        </div>

        <div class="clinic">
            <h3>🕘 Schedule</h3>

            <div class="row">
                <div class="row-icon">📅</div>
                <div>
                    <strong>Days</strong>
                    <span>Tuesday • Thursday • Saturday</span>
                </div>
            </div>

            <div class="row">
                <div class="row-icon">⏰</div>
                <div>
                    <strong>Time</strong>
                    <span>9:00 AM – 4:00 PM</span>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="assistance">
    <div class="assistance-box">

        <div class="kicker" style="color:#e4d7ff">
            Patient Assistance
        </div>

        <h2>Need a little help?</h2>

        <p>
            Tell the clinic what you need. Your request will appear on the
            protected staff dashboard so the clinic team can follow up.
        </p>

        <form class="assistance-form" method="post" action="/request-assistance">

            <div>
                <label for="patient_name">Name</label>
                <input
                    id="patient_name"
                    name="patient_name"
                    required
                    maxlength="120"
                    placeholder="Your name"
                >
            </div>

            <div>
                <label for="contact">Contact</label>
                <input
                    id="contact"
                    name="contact"
                    required
                    maxlength="160"
                    placeholder="Phone or email"
                >
            </div>

            <div>
                <label for="urgency">How urgent is this?</label>
                <select id="urgency" name="urgency">
                    <option>Normal</option>
                    <option>Needs attention soon</option>
                    <option>Urgent</option>
                </select>
            </div>

            <div>
                <label for="preferred_language">Preferred language</label>
                <select id="preferred_language" name="preferred_language">
                    <option>English</option>
                    <option>Filipino</option>
                    <option>Visaya</option>
                </select>
            </div>

            <div class="form-full">
                <label for="concern">How can we help?</label>
                <textarea
                    id="concern"
                    name="concern"
                    required
                    maxlength="2000"
                    placeholder="Tell the clinic what you need assistance with..."
                ></textarea>
            </div>

            <div class="form-full">
                <button type="submit" class="btn" style="background:#fff;color:#5b21b6">
                    Send Assistance Request →
                </button>

                <div class="form-note">
                    Please do not use this form for emergencies. For an immediate
                    medical or safety emergency, contact your local emergency services.
                </div>
            </div>

        </form>

    </div>
</section>
"""

    return page("Home", content)


@app.post("/request-assistance")
def request_assistance():
    patient_name = clean_text(request.form.get("patient_name"), 120)
    contact = clean_text(request.form.get("contact"), 160)
    concern = clean_text(request.form.get("concern"), 2000)
    urgency = clean_text(request.form.get("urgency"), 40)
    preferred_language = clean_text(
        request.form.get("preferred_language"),
        30,
    )

    allowed_urgencies = {
        "Normal",
        "Needs attention soon",
        "Urgent",
    }

    allowed_languages = {
        "English",
        "Filipino",
        "Visaya",
    }

    if urgency not in allowed_urgencies:
        urgency = "Normal"

    if preferred_language not in allowed_languages:
        preferred_language = "English"

    if not patient_name or not contact or not concern:
        flash(
            "Please complete your name, contact information, and assistance request.",
            "danger",
        )
        return redirect(url_for("home", _anchor="assistance"))

    now = datetime.utcnow().isoformat(timespec="seconds")

    db = get_db()
    db.execute(
        """
        INSERT INTO assistance_requests
        (
            patient_name,
            contact,
            concern,
            urgency,
            preferred_language,
            status,
            staff_note,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'New', '', ?, ?)
        """,
        (
            patient_name,
            contact,
            concern,
            urgency,
            preferred_language,
            now,
            now,
        ),
    )
    db.commit()
    db.close()

    flash(
        "Your assistance request has been sent. The clinic team can now see it.",
        "success",
    )

    return redirect(url_for("home", _anchor="assistance"))


@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if session.get("staff_logged_in"):
        return redirect(url_for("staff_dashboard"))

    if request.method == "POST":
        username = clean_text(request.form.get("username"), 80)
        password = request.form.get("password", "")

        db = get_db()
        staff = db.execute(
            """
            SELECT *
            FROM staff
            WHERE username = ?
            AND active = 1
            """,
            (username,),
        ).fetchone()
        db.close()

        if staff and check_password_hash(
            staff["password_hash"],
            password,
        ):
            session.clear()
            session["staff_logged_in"] = True
            session["staff_id"] = staff["id"]
            session["staff_username"] = staff["username"]
            session["staff_role"] = staff["role"]

            return redirect(url_for("staff_dashboard"))

        flash("Invalid username or password.", "danger")

    content = """
<div class="login-card">

    <div class="kicker">Private Clinic Area</div>

    <h1>Staff Login</h1>

    <p style="color:var(--muted);margin-bottom:22px">
        Authorized clinic staff only.
    </p>

    <form method="post">

        <div class="field">
            <label for="username">Username</label>
            <input id="username" name="username" required autocomplete="username">
        </div>

        <div class="field">
            <label for="password">Password</label>
            <input id="password" name="password" type="password" required autocomplete="current-password">
        </div>

        <button class="btn btn-primary" type="submit" style="width:100%">
            🔐 Log In
        </button>

        <div class="note">
            Set ADMIN_PASSWORD in Render environment variables before using this in production.
        </div>

    </form>
</div>
"""

    return page("Staff Login", content)


@app.route("/staff/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/staff")
@app.route("/staff/dashboard")
@staff_required
def staff_dashboard():
    db = get_db()

    new_count = db.execute(
        "SELECT COUNT(*) FROM assistance_requests WHERE status = 'New'"
    ).fetchone()[0]

    active_count = db.execute(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status != 'Resolved'
        """
    ).fetchone()[0]

    resolved_count = db.execute(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status = 'Resolved'
        """
    ).fetchone()[0]

    requests = db.execute(
        """
        SELECT *
        FROM assistance_requests
        ORDER BY
            CASE WHEN status = 'New' THEN 0 ELSE 1 END,
            CASE WHEN urgency = 'Urgent' THEN 0 ELSE 1 END,
            created_at DESC
        LIMIT 100
        """
    ).fetchall()

    db.close()

    request_cards = ""

    for item in requests:
        urgent_class = (
            "badge-urgent"
            if item["urgency"] == "Urgent"
            else ""
        )

        request_class = (
            "request new"
            if item["status"] == "New"
            else "request"
        )

        note_form = f"""
        <form method="post" action="/staff/request/{item['id']}/note">
            <div class="field">
                <label>Staff note</label>
                <textarea
                    name="staff_note"
                    maxlength="2000"
                    placeholder="Internal follow-up note..."
                >{item['staff_note']}</textarea>
            </div>

            <div class="request-actions">
                <button class="btn btn-secondary" type="submit">
                    Save Note
                </button>
        """

        if item["status"] == "New":
            note_form += f"""
                <button
                    class="btn btn-primary"
                    type="submit"
                    formaction="/staff/request/{item['id']}/status/Seen"
                >
                    Mark Seen
                </button>
            """

        elif item["status"] == "Seen":
            note_form += f"""
                <button
                    class="btn btn-primary"
                    type="submit"
                    formaction="/staff/request/{item['id']}/status/In Progress"
                >
                    Mark In Progress
                </button>
            """

        if item["status"] != "Resolved":
            note_form += f"""
                <button
                    class="btn"
                    type="submit"
                    formaction="/staff/request/{item['id']}/status/Resolved"
                    style="background:#15803d"
                >
                    Mark Resolved
                </button>
            """

        note_form += """
            </div>
        </form>
        """

        request_cards += f"""
<div class="{request_class}">

    <div class="request-top">

        <div>
            <div class="request-name">
                {item["patient_name"]}
            </div>

            <div class="request-time">
                Submitted {item["created_at"].replace("T", " ")} UTC
            </div>
        </div>

        <div class="badges">

            <span class="badge-status">
                {item["status"]}
            </span>

            <span class="badge-status {urgent_class}">
                {item["urgency"]}
            </span>

        </div>

    </div>


    <div class="request-grid">

        <div class="request-field">
            <strong>Contact</strong>
            <span>{item["contact"]}</span>
        </div>

        <div class="request-field">
            <strong>Language</strong>
            <span>{item["preferred_language"]}</span>
        </div>

        <div class="request-field">
            <strong>Request ID</strong>
            <span>#{item["id"]}</span>
        </div>

    </div>


    <div class="request-field">
        <strong>What they need</strong>
        <span>{item["concern"]}</span>
    </div>


    <div style="margin-top:15px">
        {note_form}
    </div>

</div>
"""

    if not requests:
        request_cards = """
        <div class="empty">
            <div style="font-size:38px;margin-bottom:8px">💜</div>
            <strong>No assistance requests yet.</strong>
            <p>New patient assistance requests will appear here automatically.</p>
        </div>
        """

    content = f"""
<section class="staff-header">

    <div class="staff-title">

        <div>
            <div class="kicker">Protected Clinic Area</div>
            <h1>Staff Dashboard</h1>
            <p>
                Welcome, {session.get("staff_username", "Staff")}.
                Monitor patients who have asked the clinic for assistance.
            </p>
        </div>

        <div class="staff-actions">
            <a class="btn btn-secondary" href="{url_for('home')}">
                Public Site
            </a>

            <a class="btn btn-primary" href="{url_for('logout')}">
                Log Out
            </a>
        </div>

    </div>

</section>


<section>

    <div class="stats">

        <div class="stat">
            <span class="stat-number" id="liveNewCount">{new_count}</span>
            <span class="stat-label">New assistance requests</span>
        </div>

        <div class="stat">
            <span class="stat-number">{active_count}</span>
            <span class="stat-label">Active requests</span>
        </div>

        <div class="stat">
            <span class="stat-number">{resolved_count}</span>
            <span class="stat-label">Resolved requests</span>
        </div>

    </div>


    <div class="card" style="
        padding:24px;
        background:var(--card);
        border:1px solid var(--border);
        border-radius:20px;
        margin-bottom:16px;
    ">

        <strong>
            🔴 Live monitoring
        </strong>

        <span style="color:var(--muted)">
            This dashboard checks for new assistance requests every 10 seconds.
        </span>

    </div>


    <div class="requests">
        {request_cards}
    </div>

</section>
"""

    return page("Staff Dashboard", content, staff=True)


@app.route("/staff/status")
@staff_required
def staff_status():
    return jsonify(
        {
            "new_count": get_new_count(),
        }
    )


@app.post("/staff/request/<int:request_id>/status/<status>")
@staff_required
def update_status(request_id, status):
    allowed = {
        "New",
        "Seen",
        "In Progress",
        "Resolved",
    }

    if status not in allowed:
        flash("Invalid request status.", "danger")
        return redirect(url_for("staff_dashboard"))

    db = get_db()

    exists = db.execute(
        "SELECT id FROM assistance_requests WHERE id = ?",
        (request_id,),
    ).fetchone()

    if exists is None:
        db.close()
        flash("That assistance request no longer exists.", "danger")
        return redirect(url_for("staff_dashboard"))

    now = datetime.utcnow().isoformat(timespec="seconds")

    db.execute(
        """
        UPDATE assistance_requests
        SET status = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            status,
            now,
            request_id,
        ),
    )

    db.commit()
    db.close()

    flash(
        f"Request #{request_id} marked as {status}.",
        "success",
    )

    return redirect(url_for("staff_dashboard"))


@app.post("/staff/request/<int:request_id>/note")
@staff_required
def update_note(request_id):
    note = clean_text(
        request.form.get("staff_note"),
        2000,
    )

    db = get_db()

    db.execute(
        """
        UPDATE assistance_requests
        SET staff_note = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            note,
            datetime.utcnow().isoformat(timespec="seconds"),
            request_id,
        ),
    )

    db.commit()
    db.close()

    flash(
        f"Staff note saved for request #{request_id}.",
        "success",
    )

    return redirect(url_for("staff_dashboard"))


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )
