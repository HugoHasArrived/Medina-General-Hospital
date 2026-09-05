from flask import Flask, request, redirect, url_for, session, jsonify, render_template_string
from functools import wraps
from datetime import datetime
import os
import secrets

app = Flask(__name__)

# ---------------------------------------------------------
# FLASK CONFIGURATION
# ---------------------------------------------------------

app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Staff credentials.
# For production, change these through Render Environment Variables.
STAFF_USERNAME = os.environ.get("STAFF_USERNAME", "staff")
STAFF_PASSWORD = os.environ.get("STAFF_PASSWORD", "medina123")

# In-memory assistance requests.
# These remain while the Render instance is running.
assistance_requests = []


# ---------------------------------------------------------
# TRANSLATIONS
# ---------------------------------------------------------

TRANSLATIONS = {
    "en": {
        "language": "English",
        "filipino": "Filipino",
        "visaya": "Visaya",

        "home": "Home",
        "about": "About the Doctor",
        "services": "Services",
        "clinic": "Clinic",
        "assistance": "Need Assistance?",
        "staff": "Staff",
        "login": "Staff Login",
        "logout": "Log Out",

        "hero_small": "PSYCHIATRIST • PHYSICIAN",
        "hero_title": "Your Mental Health Matters.",
        "hero_text": "Compassionate psychiatric care focused on understanding you, supporting you, and helping you move forward.",
        "book": "View Clinic Schedule",
        "help": "I Need Assistance",

        "about_title": "Meet Dr. Bebie Queen Lucelle R. Tagupa",
        "about_subtitle": "Licensed Physician & Psychiatrist",
        "about_text_1": "Dr. Bebie Queen Lucelle R. Tagupa is a licensed physician and psychiatrist. She earned her Bachelor’s degree in Medical Technology from Velez College and is also a licensed Medical Technologist.",
        "about_text_2": "She proceeded to study Medicine at Xavier University – Ateneo de Cagayan. She completed her post-graduate internship at Davao Doctors Hospital and finished her residency training in Psychiatry at the Southern Philippines Medical Center – Institute of Psychiatry and Behavioral Medicine.",
        "about_text_3": "During her final year of training, she served as Chief Resident and was awarded Most Outstanding Resident in Psychiatry during her graduation.",
        "about_text_4": "Dr. Tagupa provides psychiatric evaluation and treatment for a wide range of mental health conditions. She is committed to providing compassionate, patient-centered care to help individuals improve their mental well-being and overall quality of life.",

        "credentials": "Professional Background",
        "medical_technology": "Medical Technology",
        "medical_technology_desc": "Bachelor’s Degree • Velez College",
        "licensed_medtech": "Licensed Medical Technologist",
        "medicine": "Medicine",
        "medicine_desc": "Xavier University – Ateneo de Cagayan",
        "psychiatry": "Psychiatry Residency",
        "psychiatry_desc": "Southern Philippines Medical Center",
        "award": "Most Outstanding Resident",
        "award_desc": "Psychiatry • Graduation Award",

        "services_title": "Psychiatric Care",
        "services_intro": "Professional, compassionate support for different mental health needs.",
        "service_1": "Psychiatric Evaluation",
        "service_1_desc": "A professional assessment to better understand your mental health needs.",
        "service_2": "Treatment & Management",
        "service_2_desc": "Personalized psychiatric care based on your individual needs.",
        "service_3": "Mental Well-being Support",
        "service_3_desc": "Compassionate guidance focused on improving your quality of life.",

        "clinic_title": "Visit the Clinic",
        "clinic_name": "Medina General Hospital",
        "clinic_location": "Outpatient Department (OPD), Door 2",
        "schedule": "Clinic Schedule",
        "schedule_days": "Tuesday • Thursday • Saturday",
        "schedule_time": "9:00 AM – 4:00 PM",

        "assistance_title": "Do You Need Assistance?",
        "assistance_text": "Let the clinic staff know what kind of assistance you need. Your request will appear on the staff dashboard.",
        "name": "Name",
        "name_placeholder": "Enter your name",
        "contact": "Contact Information",
        "contact_placeholder": "Phone number or email",
        "request_type": "What do you need?",
        "request_placeholder": "Choose an option",
        "appointment": "Appointment Assistance",
        "clinic_info": "Clinic Information",
        "general_help": "General Assistance",
        "other": "Other",
        "message": "Message",
        "message_placeholder": "Tell us how we can help you...",
        "submit": "Send Assistance Request",
        "success": "Your assistance request has been sent successfully.",
        "required": "Please complete all required fields.",

        "staff_login_title": "Staff Portal",
        "staff_login_text": "Authorized clinic staff only.",
        "username": "Username",
        "password": "Password",
        "sign_in": "Sign In",
        "invalid_login": "Invalid username or password.",

        "dashboard": "Staff Dashboard",
        "dashboard_intro": "Review patient assistance requests and respond to those who need help.",
        "pending": "Pending",
        "handled": "Handled",
        "all_requests": "All Requests",
        "no_requests": "There are no assistance requests yet.",
        "patient": "Patient",
        "request": "Request",
        "time": "Time",
        "status": "Status",
        "action": "Action",
        "mark_handled": "Mark as Handled",
        "handled_label": "Handled",
        "pending_label": "Pending",
        "back_home": "Back to Website",

        "footer_text": "Compassionate care. Better understanding. A healthier tomorrow.",
        "privacy": "Patient information should be handled confidentially by authorized clinic personnel."
    },

    "fil": {
        "language": "Filipino",
        "filipino": "Filipino",
        "visaya": "Visaya",

        "home": "Home",
        "about": "Tungkol sa Doktor",
        "services": "Mga Serbisyo",
        "clinic": "Klinika",
        "assistance": "Kailangan ng Tulong?",
        "staff": "Staff",
        "login": "Staff Login",
        "logout": "Mag-Log Out",

        "hero_small": "PSYCHIATRIST • PHYSICIAN",
        "hero_title": "Mahalaga ang Iyong Mental Health.",
        "hero_text": "Maunawain at maalagang psychiatric care na nakatuon sa iyong kalagayan, pangangailangan, at pagbuti ng iyong kalidad ng buhay.",
        "book": "Tingnan ang Schedule",
        "help": "Kailangan Ko ng Tulong",

        "about_title": "Kilalanin si Dr. Bebie Queen Lucelle R. Tagupa",
        "about_subtitle": "Licensed Physician at Psychiatrist",
        "about_text_1": "Si Dr. Bebie Queen Lucelle R. Tagupa ay isang licensed physician at psychiatrist. Natapos niya ang kanyang Bachelor’s degree sa Medical Technology sa Velez College at isa rin siyang licensed Medical Technologist.",
        "about_text_2": "Nag-aral siya ng Medicine sa Xavier University – Ateneo de Cagayan. Natapos niya ang kanyang post-graduate internship sa Davao Doctors Hospital at ang residency training niya sa Psychiatry sa Southern Philippines Medical Center – Institute of Psychiatry and Behavioral Medicine.",
        "about_text_3": "Sa kanyang huling taon ng training, nagsilbi siya bilang Chief Resident at ginawaran bilang Most Outstanding Resident in Psychiatry sa kanyang graduation.",
        "about_text_4": "Nagbibigay si Dr. Tagupa ng psychiatric evaluation at treatment para sa iba't ibang mental health conditions. Nakatuon siya sa compassionate at patient-centered care upang matulungan ang bawat pasyente na mapabuti ang kanilang mental well-being at kalidad ng buhay.",

        "credentials": "Propesyonal na Background",
        "medical_technology": "Medical Technology",
        "medical_technology_desc": "Bachelor’s Degree • Velez College",
        "licensed_medtech": "Licensed Medical Technologist",
        "medicine": "Medicine",
        "medicine_desc": "Xavier University – Ateneo de Cagayan",
        "psychiatry": "Psychiatry Residency",
        "psychiatry_desc": "Southern Philippines Medical Center",
        "award": "Most Outstanding Resident",
        "award_desc": "Psychiatry • Graduation Award",

        "services_title": "Psychiatric Care",
        "services_intro": "Propesyonal at maalagang suporta para sa iba't ibang pangangailangan sa mental health.",
        "service_1": "Psychiatric Evaluation",
        "service_1_desc": "Propesyonal na pagsusuri upang mas maunawaan ang iyong mental health needs.",
        "service_2": "Treatment at Management",
        "service_2_desc": "Personalized psychiatric care batay sa iyong sariling pangangailangan.",
        "service_3": "Mental Well-being Support",
        "service_3_desc": "Maunawain at maalagang gabay para sa mas magandang kalidad ng buhay.",

        "clinic_title": "Bumisita sa Klinika",
        "clinic_name": "Medina General Hospital",
        "clinic_location": "Outpatient Department (OPD), Door 2",
        "schedule": "Schedule ng Klinika",
        "schedule_days": "Martes • Huwebes • Sabado",
        "schedule_time": "9:00 AM – 4:00 PM",

        "assistance_title": "Kailangan Mo ba ng Tulong?",
        "assistance_text": "Sabihin sa clinic staff kung anong tulong ang kailangan mo. Makikita ng staff ang iyong request sa kanilang dashboard.",
        "name": "Pangalan",
        "name_placeholder": "Ilagay ang iyong pangalan",
        "contact": "Contact Information",
        "contact_placeholder": "Phone number o email",
        "request_type": "Ano ang kailangan mo?",
        "request_placeholder": "Pumili ng option",
        "appointment": "Tulong sa Appointment",
        "clinic_info": "Impormasyon tungkol sa Klinika",
        "general_help": "General Assistance",
        "other": "Iba pa",
        "message": "Mensahe",
        "message_placeholder": "Sabihin kung paano ka namin matutulungan...",
        "submit": "Ipadala ang Request",
        "success": "Matagumpay na naipadala ang iyong assistance request.",
        "required": "Pakikumpleto ang lahat ng kinakailangang fields.",

        "staff_login_title": "Staff Portal",
        "staff_login_text": "Para lamang sa authorized clinic staff.",
        "username": "Username",
        "password": "Password",
        "sign_in": "Mag-Sign In",
        "invalid_login": "Mali ang username o password.",

        "dashboard": "Staff Dashboard",
        "dashboard_intro": "Tingnan ang mga assistance request ng mga pasyente at tugunan ang mga nangangailangan ng tulong.",
        "pending": "Pending",
        "handled": "Handled",
        "all_requests": "Lahat ng Requests",
        "no_requests": "Wala pang assistance requests.",
        "patient": "Pasyente",
        "request": "Request",
        "time": "Oras",
        "status": "Status",
        "action": "Action",
        "mark_handled": "Markahan bilang Handled",
        "handled_label": "Handled",
        "pending_label": "Pending",
        "back_home": "Bumalik sa Website",

        "footer_text": "Maalagang serbisyo. Mas mahusay na pag-unawa. Mas magandang bukas.",
        "privacy": "Ang impormasyon ng pasyente ay dapat panatilihing kumpidensyal ng authorized clinic personnel."
    },

    "ceb": {
        "language": "Visaya",
        "filipino": "Filipino",
        "visaya": "Visaya",

        "home": "Home",
        "about": "Mahitungod sa Doktor",
        "services": "Mga Serbisyo",
        "clinic": "Klinika",
        "assistance": "Kinahanglan ba og Tabang?",
        "staff": "Staff",
        "login": "Staff Login",
        "logout": "Log Out",

        "hero_small": "PSYCHIATRIST • PHYSICIAN",
        "hero_title": "Importante ang Imong Mental Health.",
        "hero_text": "Malumo ug masinabtanon nga psychiatric care nga naka-focus sa imong kahimtang, panginahanglan, ug kalidad sa kinabuhi.",
        "book": "Tan-awa ang Schedule",
        "help": "Kinahanglan Ko og Tabang",

        "about_title": "Ilaila si Dr. Bebie Queen Lucelle R. Tagupa",
        "about_subtitle": "Licensed Physician ug Psychiatrist",
        "about_text_1": "Si Dr. Bebie Queen Lucelle R. Tagupa usa ka licensed physician ug psychiatrist. Nakuha niya ang iyang Bachelor’s degree sa Medical Technology gikan sa Velez College ug usa usab siya ka licensed Medical Technologist.",
        "about_text_2": "Nagpadayon siya sa pagtuon og Medicine sa Xavier University – Ateneo de Cagayan. Nahuman niya ang iyang post-graduate internship sa Davao Doctors Hospital ug ang iyang residency training sa Psychiatry sa Southern Philippines Medical Center – Institute of Psychiatry and Behavioral Medicine.",
        "about_text_3": "Sa iyang katapusang tuig sa training, nagsilbi siya isip Chief Resident ug gihatagan og award nga Most Outstanding Resident in Psychiatry sa iyang graduation.",
        "about_text_4": "Naghatag si Dr. Tagupa og psychiatric evaluation ug treatment alang sa lain-laing mental health conditions. Nagtuon siya sa compassionate ug patient-centered care aron matabangan ang mga pasyente nga mapauswag ang ilang mental well-being ug kalidad sa kinabuhi.",

        "credentials": "Professional Background",
        "medical_technology": "Medical Technology",
        "medical_technology_desc": "Bachelor’s Degree • Velez College",
        "licensed_medtech": "Licensed Medical Technologist",
        "medicine": "Medicine",
        "medicine_desc": "Xavier University – Ateneo de Cagayan",
        "psychiatry": "Psychiatry Residency",
        "psychiatry_desc": "Southern Philippines Medical Center",
        "award": "Most Outstanding Resident",
        "award_desc": "Psychiatry • Graduation Award",

        "services_title": "Psychiatric Care",
        "services_intro": "Propesyonal ug masinabtanon nga suporta alang sa lain-laing mental health needs.",
        "service_1": "Psychiatric Evaluation",
        "service_1_desc": "Propesyonal nga assessment aron masabtan ang imong mental health needs.",
        "service_2": "Treatment ug Management",
        "service_2_desc": "Personalized psychiatric care base sa imong kaugalingong panginahanglan.",
        "service_3": "Mental Well-being Support",
        "service_3_desc": "Masinabtanon nga suporta para sa mas maayong kalidad sa kinabuhi.",

        "clinic_title": "Bisita sa Klinika",
        "clinic_name": "Medina General Hospital",
        "clinic_location": "Outpatient Department (OPD), Door 2",
        "schedule": "Schedule sa Klinika",
        "schedule_days": "Martes • Huwebes • Sabado",
        "schedule_time": "9:00 AM – 4:00 PM",

        "assistance_title": "Kinahanglan ba Nimo og Tabang?",
        "assistance_text": "Sultihi ang clinic staff kung unsa nga tabang ang imong gikinahanglan. Makita sa staff ang imong request sa ilang dashboard.",
        "name": "Ngalan",
        "name_placeholder": "Ibutang ang imong ngalan",
        "contact": "Contact Information",
        "contact_placeholder": "Phone number o email",
        "request_type": "Unsa imong gikinahanglan?",
        "request_placeholder": "Pilia ang option",
        "appointment": "Tabang sa Appointment",
        "clinic_info": "Impormasyon sa Klinika",
        "general_help": "General Assistance",
        "other": "Uban pa",
        "message": "Mensahe",
        "message_placeholder": "Isulti kung unsaon namo pagtabang kanimo...",
        "submit": "Ipadala ang Request",
        "success": "Malampuson nga naipadala ang imong assistance request.",
        "required": "Palihog kompletuha ang tanang gikinahanglang fields.",

        "staff_login_title": "Staff Portal",
        "staff_login_text": "Alang lamang sa authorized clinic staff.",
        "username": "Username",
        "password": "Password",
        "sign_in": "Sign In",
        "invalid_login": "Sayop ang username o password.",

        "dashboard": "Staff Dashboard",
        "dashboard_intro": "Tan-awa ang mga assistance request sa mga pasyente ug tabangi ang mga nanginahanglan.",
        "pending": "Pending",
        "handled": "Handled",
        "all_requests": "Tanang Requests",
        "no_requests": "Wala pay assistance requests.",
        "patient": "Pasyente",
        "request": "Request",
        "time": "Oras",
        "status": "Status",
        "action": "Action",
        "mark_handled": "Markahi isip Handled",
        "handled_label": "Handled",
        "pending_label": "Pending",
        "back_home": "Balik sa Website",

        "footer_text": "Malumo nga pag-atiman. Mas maayong pagsabot. Mas maayong kaugmaon.",
        "privacy": "Ang impormasyon sa pasyente kinahanglan nga kumpidensyal ug dumalahon lamang sa authorized clinic personnel."
    }
}


def get_language():
    lang = session.get("language", "en")
    if lang not in TRANSLATIONS:
        lang = "en"
    return lang


@app.context_processor
def inject_translations():
    lang = get_language()
    return {
        "t": TRANSLATIONS[lang],
        "lang": lang
    }


# ---------------------------------------------------------
# STAFF AUTHENTICATION
# ---------------------------------------------------------

def staff_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("staff_logged_in"):
            return redirect(url_for("staff_login"))
        return function(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------
# MAIN WEBSITE TEMPLATE
# ---------------------------------------------------------

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dr. Bebie Tagupa | Psychiatrist</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Arial,
                sans-serif;

            background: var(--bg);
            color: var(--text);
            transition: background 0.3s ease, color 0.3s ease;
            min-height: 100vh;
        }

        :root {
            --purple: #7c3aed;
            --purple-dark: #5b21b6;
            --purple-light: #a78bfa;
            --purple-soft: #ede9fe;

            --bg: #faf8ff;
            --surface: #ffffff;
            --surface-2: #f5f3ff;
            --text: #20152f;
            --muted: #6b6175;
            --border: #e7def5;
            --shadow: 0 15px 45px rgba(76, 29, 149, 0.12);
        }

        body.dark {
            --bg: #110b18;
            --surface: #1b1224;
            --surface-2: #24162f;
            --text: #f8f5ff;
            --muted: #c5b9cf;
            --border: #382447;
            --shadow: 0 15px 45px rgba(0, 0, 0, 0.35);
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        button,
        input,
        select,
        textarea {
            font: inherit;
        }

        button {
            cursor: pointer;
        }

        .container {
            width: min(1120px, 92%);
            margin: 0 auto;
        }

        .center {
            text-align: center;
        }

        /* NAVBAR */

        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: color-mix(in srgb, var(--surface) 90%, transparent);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid var(--border);
        }

        .nav-inner {
            min-height: 76px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-weight: 800;
            color: var(--text);
        }

        .brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--purple), var(--purple-dark));
            color: white;
            display: grid;
            place-items: center;
            font-size: 20px;
            box-shadow: 0 8px 22px rgba(124, 58, 237, 0.3);
        }

        .brand-text {
            line-height: 1.1;
        }

        .brand-name {
            font-size: 15px;
        }

        .brand-sub {
            font-size: 11px;
            color: var(--muted);
            font-weight: 600;
            margin-top: 3px;
        }

        .nav-links {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .nav-links a {
            padding: 9px 12px;
            border-radius: 10px;
            color: var(--muted);
            font-size: 14px;
            font-weight: 600;
            transition: 0.2s;
        }

        .nav-links a:hover {
            background: var(--surface-2);
            color: var(--purple);
        }

        .nav-actions {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .control {
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            border-radius: 11px;
            padding: 9px 11px;
            font-size: 13px;
            font-weight: 700;
        }

        .control:hover {
            border-color: var(--purple-light);
        }

        .mobile-menu {
            display: none;
        }

        /* HERO */

        .hero {
            position: relative;
            overflow: hidden;
            padding: 100px 0 90px;
            background:
                radial-gradient(circle at 15% 20%, rgba(124, 58, 237, 0.15), transparent 28%),
                radial-gradient(circle at 85% 20%, rgba(167, 139, 250, 0.15), transparent 28%);
        }

        .hero-content {
            max-width: 850px;
            margin: 0 auto;
            text-align: center;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 15px;
            border-radius: 999px;
            background: var(--purple-soft);
            color: var(--purple-dark);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 24px;
        }

        body.dark .eyebrow {
            background: #33204b;
            color: #d8c6ff;
        }

        .hero h1 {
            font-size: clamp(42px, 7vw, 76px);
            line-height: 0.98;
            letter-spacing: -0.05em;
            max-width: 800px;
            margin: 0 auto 24px;
        }

        .gradient-text {
            background: linear-gradient(
                135deg,
                var(--purple),
                #a855f7,
                var(--purple-dark)
            );
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero p {
            max-width: 680px;
            margin: 0 auto;
            color: var(--muted);
            font-size: 18px;
            line-height: 1.8;
        }

        .hero-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 34px;
        }

        .btn {
            border: 0;
            border-radius: 13px;
            padding: 14px 22px;
            font-weight: 800;
            transition: transform 0.2s, box-shadow 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--purple), var(--purple-dark));
            color: white;
            box-shadow: 0 10px 25px rgba(124, 58, 237, 0.25);
        }

        .btn-secondary {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text);
        }

        /* SECTION */

        section {
            padding: 90px 0;
        }

        .section-heading {
            max-width: 720px;
            margin: 0 auto 50px;
            text-align: center;
        }

        .section-heading .mini {
            color: var(--purple);
            font-size: 13px;
            font-weight: 900;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .section-heading h2 {
            font-size: clamp(32px, 5vw, 50px);
            letter-spacing: -0.035em;
            margin-bottom: 15px;
        }

        .section-heading p {
            color: var(--muted);
            line-height: 1.8;
        }

        /* DOCTOR */

        .doctor-grid {
            display: grid;
            grid-template-columns: minmax(280px, 400px) 1fr;
            align-items: center;
            gap: 70px;
        }

        .doctor-photo-wrap {
            text-align: center;
        }

        .doctor-photo {
            width: min(100%, 380px);
            aspect-ratio: 1 / 1.08;
            object-fit: cover;
            object-position: center;
            border-radius: 30px;
            display: block;
            margin: 0 auto;
            box-shadow: var(--shadow);
            border: 7px solid var(--surface);
            outline: 1px solid var(--border);
        }

        .doctor-info {
            text-align: center;
        }

        .doctor-info h2 {
            font-size: clamp(30px, 4vw, 45px);
            line-height: 1.1;
            margin-bottom: 10px;
        }

        .doctor-role {
            color: var(--purple);
            font-weight: 800;
            margin-bottom: 25px;
        }

        .doctor-info p {
            color: var(--muted);
            line-height: 1.85;
            margin: 0 auto 16px;
            max-width: 700px;
        }

        /* CREDENTIALS */

        .credential-grid {
            margin-top: 50px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
        }

        .credential {
            text-align: center;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 25px 18px;
            box-shadow: 0 8px 25px rgba(76, 29, 149, 0.05);
        }

        .credential-icon {
            width: 50px;
            height: 50px;
            margin: 0 auto 15px;
            border-radius: 15px;
            display: grid;
            place-items: center;
            background: var(--purple-soft);
            font-size: 22px;
        }

        body.dark .credential-icon {
            background: #33204b;
        }

        .credential h3 {
            font-size: 16px;
            margin-bottom: 8px;
        }

        .credential p {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        /* SERVICES */

        .services-section {
            background: var(--surface-2);
        }

        .service-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .service-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 32px 25px;
            text-align: center;
            transition: 0.25s;
        }

        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--purple-light);
        }

        .service-icon {
            font-size: 35px;
            margin-bottom: 18px;
        }

        .service-card h3 {
            font-size: 20px;
            margin-bottom: 10px;
        }

        .service-card p {
            color: var(--muted);
            line-height: 1.7;
            font-size: 14px;
        }

        /* CLINIC */

        .clinic-card {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
            background:
                linear-gradient(
                    135deg,
                    var(--surface),
                    var(--surface-2)
                );
            border: 1px solid var(--border);
            border-radius: 30px;
            padding: 45px 30px;
            box-shadow: var(--shadow);
        }

        .clinic-symbol {
            width: 70px;
            height: 70px;
            margin: 0 auto 20px;
            border-radius: 22px;
            background: linear-gradient(135deg, var(--purple), var(--purple-dark));
            color: white;
            display: grid;
            place-items: center;
            font-size: 32px;
        }

        .clinic-card h2 {
            font-size: 32px;
            margin-bottom: 8px;
        }

        .clinic-address {
            color: var(--muted);
            margin-bottom: 30px;
        }

        .schedule-box {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 20px 30px;
            min-width: min(100%, 400px);
        }

        .schedule-box strong {
            color: var(--purple);
            margin-bottom: 7px;
        }

        .schedule-box span {
            font-weight: 800;
        }

        .schedule-time {
            margin-top: 5px;
            color: var(--muted);
        }

        /* ASSISTANCE */

        .assistance-section {
            background: var(--surface-2);
        }

        .form-card {
            max-width: 760px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 28px;
            padding: 35px;
            box-shadow: var(--shadow);
        }

        .form-card-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .form-card-header h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .form-card-header p {
            color: var(--muted);
            line-height: 1.7;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }

        .form-group {
            text-align: center;
        }

        .form-group.full {
            grid-column: 1 / -1;
        }

        .form-group label {
            display: block;
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .form-control {
            width: 100%;
            border: 1px solid var(--border);
            background: var(--surface-2);
            color: var(--text);
            border-radius: 13px;
            padding: 13px 15px;
            outline: none;
            text-align: center;
            transition: 0.2s;
        }

        textarea.form-control {
            min-height: 120px;
            resize: vertical;
        }

        .form-control:focus {
            border-color: var(--purple);
            box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.1);
        }

        .submit-row {
            text-align: center;
            margin-top: 25px;
        }

        .alert {
            max-width: 760px;
            margin: 0 auto 20px;
            padding: 15px;
            border-radius: 14px;
            text-align: center;
            font-weight: 700;
        }

        .alert-success {
            background: #dcfce7;
            color: #166534;
        }

        body.dark .alert-success {
            background: #163b27;
            color: #b5f5c8;
        }

        .alert-error {
            background: #fee2e2;
            color: #991b1b;
        }

        body.dark .alert-error {
            background: #421d1d;
            color: #ffc2c2;
        }

        /* FOOTER */

        footer {
            background: #160d20;
            color: white;
            padding: 55px 0;
            text-align: center;
        }

        footer .footer-brand {
            font-size: 21px;
            font-weight: 900;
            margin-bottom: 12px;
        }

        footer p {
            color: #c7b9d0;
            max-width: 600px;
            margin: 0 auto 18px;
            line-height: 1.7;
        }

        .privacy {
            font-size: 12px;
            color: #9f91a9;
        }

        /* RESPONSIVE */

        @media (max-width: 950px) {
            .nav-links {
                display: none;
            }

            .mobile-menu {
                display: block;
            }

            .doctor-grid {
                grid-template-columns: 1fr;
                gap: 40px;
            }

            .credential-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .service-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 650px) {
            .nav-inner {
                min-height: 68px;
            }

            .brand-sub {
                display: none;
            }

            .brand-name {
                font-size: 13px;
            }

            .nav-actions {
                gap: 5px;
            }

            .control {
                padding: 8px;
            }

            .hero {
                padding: 75px 0;
            }

            section {
                padding: 65px 0;
            }

            .credential-grid {
                grid-template-columns: 1fr;
            }

            .form-card {
                padding: 23px 17px;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .form-group.full {
                grid-column: auto;
            }

            .hero-buttons {
                flex-direction: column;
            }

            .hero-buttons .btn {
                width: 100%;
                max-width: 330px;
            }

            .clinic-card {
                padding: 35px 20px;
            }
        }
    </style>
</head>

<body>

    <!-- NAVBAR -->
    <header class="navbar">
        <div class="container nav-inner">

            <a href="#home" class="brand">
                <div class="brand-icon">🧠</div>

                <div class="brand-text">
                    <div class="brand-name">Dr. Bebie Tagupa</div>
                    <div class="brand-sub">PSYCHIATRIST • PHYSICIAN</div>
                </div>
            </a>

            <nav class="nav-links">
                <a href="#home">{{ t.home }}</a>
                <a href="#about">{{ t.about }}</a>
                <a href="#services">{{ t.services }}</a>
                <a href="#clinic">{{ t.clinic }}</a>
                <a href="#assistance">{{ t.assistance }}</a>
                <a href="{{ url_for('staff_login') }}">{{ t.staff }}</a>
            </nav>

            <div class="nav-actions">

                <select
                    class="control"
                    onchange="changeLanguage(this.value)"
                    aria-label="Language"
                >
                    <option value="en" {% if lang == "en" %}selected{% endif %}>
                        🇬🇧 {{ t.language if lang == "en" else "English" }}
                    </option>

                    <option value="fil" {% if lang == "fil" %}selected{% endif %}>
                        🇵🇭 Filipino
                    </option>

                    <option value="ceb" {% if lang == "ceb" %}selected{% endif %}>
                        🇵🇭 Visaya
                    </option>
                </select>

                <button
                    class="control"
                    onclick="toggleTheme()"
                    id="themeButton"
                    title="Toggle dark/light mode"
                >
                    🌙
                </button>

            </div>
        </div>
    </header>


    <!-- HERO -->
    <main>

        <section class="hero" id="home">
            <div class="container">
                <div class="hero-content">

                    <div class="eyebrow">
                        {{ t.hero_small }}
                    </div>

                    <h1>
                        {{ t.hero_title.split(" ", 1)[0] }}
                        <span class="gradient-text">
                            {{ t.hero_title.split(" ", 1)[1] if " " in t.hero_title else "" }}
                        </span>
                    </h1>

                    <p>
                        {{ t.hero_text }}
                    </p>

                    <div class="hero-buttons">
                        <a href="#clinic" class="btn btn-primary">
                            📅 {{ t.book }}
                        </a>

                        <a href="#assistance" class="btn btn-secondary">
                            💜 {{ t.help }}
                        </a>
                    </div>

                </div>
            </div>
        </section>


        <!-- ABOUT -->
        <section id="about">
            <div class="container">

                <div class="section-heading">
                    <div class="mini">{{ t.about }}</div>
                    <h2>{{ t.about_title }}</h2>
                    <p>{{ t.about_subtitle }}</p>
                </div>

                <div class="doctor-grid">

                    <div class="doctor-photo-wrap">
                        <img
                            class="doctor-photo"
                            src="{{ url_for('static', filename='image0 (2).jpeg') }}"
                            alt="Dr. Bebie Queen Lucelle R. Tagupa"
                            onerror="this.style.display='none'; document.getElementById('photoFallback').style.display='flex';"
                        >

                        <div
                            id="photoFallback"
                            style="
                                display:none;
                                width:min(100%,380px);
                                aspect-ratio:1/1.08;
                                margin:auto;
                                border-radius:30px;
                                background:linear-gradient(135deg,#7c3aed,#5b21b6);
                                color:white;
                                align-items:center;
                                justify-content:center;
                                text-align:center;
                                padding:30px;
                                font-size:20px;
                                font-weight:800;
                            "
                        >
                            Dr. Bebie<br>
                            Queen Lucelle<br>
                            R. Tagupa
                        </div>
                    </div>

                    <div class="doctor-info">

                        <h2>Dr. Bebie Queen Lucelle R. Tagupa</h2>

                        <div class="doctor-role">
                            {{ t.about_subtitle }}
                        </div>

                        <p>{{ t.about_text_1 }}</p>
                        <p>{{ t.about_text_2 }}</p>
                        <p>{{ t.about_text_3 }}</p>
                        <p>{{ t.about_text_4 }}</p>

                    </div>

                </div>


                <div class="section-heading" style="margin-top:80px;">
                    <div class="mini">{{ t.credentials }}</div>
                    <h2>{{ t.credentials }}</h2>
                </div>

                <div class="credential-grid">

                    <div class="credential">
                        <div class="credential-icon">🎓</div>
                        <h3>{{ t.medical_technology }}</h3>
                        <p>{{ t.medical_technology_desc }}</p>
                    </div>

                    <div class="credential">
                        <div class="credential-icon">🔬</div>
                        <h3>{{ t.licensed_medtech }}</h3>
                        <p>{{ t.medical_technology_desc }}</p>
                    </div>

                    <div class="credential">
                        <div class="credential-icon">🩺</div>
                        <h3>{{ t.medicine }}</h3>
                        <p>{{ t.medicine_desc }}</p>
                    </div>

                    <div class="credential">
                        <div class="credential-icon">🏆</div>
                        <h3>{{ t.award }}</h3>
                        <p>{{ t.award_desc }}</p>
                    </div>

                </div>

            </div>
        </section>


        <!-- SERVICES -->
        <section class="services-section" id="services">

            <div class="container">

                <div class="section-heading">
                    <div class="mini">{{ t.services }}</div>
                    <h2>{{ t.services_title }}</h2>
                    <p>{{ t.services_intro }}</p>
                </div>

                <div class="service-grid">

                    <div class="service-card">
                        <div class="service-icon">🧠</div>
                        <h3>{{ t.service_1 }}</h3>
                        <p>{{ t.service_1_desc }}</p>
                    </div>

                    <div class="service-card">
                        <div class="service-icon">💜</div>
                        <h3>{{ t.service_2 }}</h3>
                        <p>{{ t.service_2_desc }}</p>
                    </div>

                    <div class="service-card">
                        <div class="service-icon">🌱</div>
                        <h3>{{ t.service_3 }}</h3>
                        <p>{{ t.service_3_desc }}</p>
                    </div>

                </div>

            </div>

        </section>


        <!-- CLINIC -->
        <section id="clinic">

            <div class="container">

                <div class="section-heading">
                    <div class="mini">{{ t.clinic }}</div>
                    <h2>{{ t.clinic_title }}</h2>
                </div>

                <div class="clinic-card">

                    <div class="clinic-symbol">🏥</div>

                    <h2>{{ t.clinic_name }}</h2>

                    <p class="clinic-address">
                        {{ t.clinic_location }}
                    </p>

                    <div class="schedule-box">
                        <strong>{{ t.schedule }}</strong>
                        <span>{{ t.schedule_days }}</span>
                        <div class="schedule-time">
                            {{ t.schedule_time }}
                        </div>
                    </div>

                </div>

            </div>

        </section>


        <!-- ASSISTANCE -->
        <section class="assistance-section" id="assistance">

            <div class="container">

                <div class="section-heading">
                    <div class="mini">{{ t.assistance }}</div>
                    <h2>{{ t.assistance_title }}</h2>
                    <p>{{ t.assistance_text }}</p>
                </div>

                {% if success %}
                    <div class="alert alert-success">
                        {{ t.success }}
                    </div>
                {% endif %}

                {% if error %}
                    <div class="alert alert-error">
                        {{ t.required }}
                    </div>
                {% endif %}

                <div class="form-card">

                    <div class="form-card-header">
                        <h2>{{ t.assistance_title }}</h2>
                        <p>{{ t.assistance_text }}</p>
                    </div>

                    <form method="POST" action="{{ url_for('submit_assistance') }}">

                        <div class="form-grid">

                            <div class="form-group">
                                <label for="name">{{ t.name }}</label>

                                <input
                                    id="name"
                                    name="name"
                                    class="form-control"
                                    type="text"
                                    placeholder="{{ t.name_placeholder }}"
                                    required
                                >
                            </div>

                            <div class="form-group">
                                <label for="contact">{{ t.contact }}</label>

                                <input
                                    id="contact"
                                    name="contact"
                                    class="form-control"
                                    type="text"
                                    placeholder="{{ t.contact_placeholder }}"
                                    required
                                >
                            </div>

                            <div class="form-group full">
                                <label for="request_type">
                                    {{ t.request_type }}
                                </label>

                                <select
                                    id="request_type"
                                    name="request_type"
                                    class="form-control"
                                    required
                                >
                                    <option value="">
                                        {{ t.request_placeholder }}
                                    </option>

                                    <option value="{{ t.appointment }}">
                                        {{ t.appointment }}
                                    </option>

                                    <option value="{{ t.clinic_info }}">
                                        {{ t.clinic_info }}
                                    </option>

                                    <option value="{{ t.general_help }}">
                                        {{ t.general_help }}
                                    </option>

                                    <option value="{{ t.other }}">
                                        {{ t.other }}
                                    </option>
                                </select>
                            </div>

                            <div class="form-group full">
                                <label for="message">
                                    {{ t.message }}
                                </label>

                                <textarea
                                    id="message"
                                    name="message"
                                    class="form-control"
                                    placeholder="{{ t.message_placeholder }}"
                                    required
                                ></textarea>
                            </div>

                        </div>

                        <div class="submit-row">
                            <button type="submit" class="btn btn-primary">
                                💜 {{ t.submit }}
                            </button>
                        </div>

                    </form>

                </div>

            </div>

        </section>

    </main>


    <!-- FOOTER -->
    <footer>

        <div class="container">

            <div class="footer-brand">
                Dr. Bebie Queen Lucelle R. Tagupa
            </div>

            <p>
                {{ t.footer_text }}
            </p>

            <div class="privacy">
                {{ t.privacy }}
            </div>

        </div>

    </footer>


    <script>

        // -------------------------------------------------
        // LANGUAGE
        // -------------------------------------------------

        function changeLanguage(language) {
            window.location.href = "/set-language/" + language;
        }


        // -------------------------------------------------
        // DARK / LIGHT MODE
        // -------------------------------------------------

        function setTheme(theme) {
            if (theme === "dark") {
                document.body.classList.add("dark");
                document.getElementById("themeButton").textContent = "☀️";
                localStorage.setItem("theme", "dark");
            } else {
                document.body.classList.remove("dark");
                document.getElementById("themeButton").textContent = "🌙";
                localStorage.setItem("theme", "light");
            }
        }


        function toggleTheme() {
            const isDark = document.body.classList.contains("dark");

            if (isDark) {
                setTheme("light");
            } else {
                setTheme("dark");
            }
        }


        const savedTheme = localStorage.getItem("theme");

        if (savedTheme) {
            setTheme(savedTheme);
        } else {
            setTheme("light");
        }


        // -------------------------------------------------
        // STAFF SESSION SAFETY
        // -------------------------------------------------

        // If someone previously logged in as staff,
        // don't leave staff state hanging around in this tab.
        //
        // sessionStorage disappears when the browser tab/window
        // is closed, unlike localStorage.

    </script>

</body>
</html>
"""


# ---------------------------------------------------------
# STAFF LOGIN TEMPLATE
# ---------------------------------------------------------

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{{ t.staff_login_title }}</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            display: flex;
            align-items: center;
            justify-content: center;

            background:
                radial-gradient(
                    circle at top,
                    #7c3aed22,
                    transparent 45%
                ),
                #faf8ff;

            color: #20152f;
            padding: 20px;
        }

        .login-card {
            width: min(440px, 100%);
            background: white;
            border: 1px solid #e7def5;
            border-radius: 28px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(76, 29, 149, 0.15);
        }

        .icon {
            width: 70px;
            height: 70px;
            border-radius: 22px;
            margin: 0 auto 20px;
            display: grid;
            place-items: center;
            font-size: 30px;
            background: linear-gradient(135deg,#7c3aed,#5b21b6);
            color: white;
        }

        h1 {
            margin: 0 0 10px;
            font-size: 32px;
        }

        .subtitle {
            color: #6b6175;
            line-height: 1.6;
            margin-bottom: 30px;
        }

        .field {
            margin-bottom: 17px;
        }

        label {
            display: block;
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 8px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #e7def5;
            border-radius: 13px;
            background: #f5f3ff;
            text-align: center;
            outline: none;
        }

        input:focus {
            border-color: #7c3aed;
            box-shadow: 0 0 0 4px #7c3aed18;
        }

        button {
            width: 100%;
            border: 0;
            padding: 14px;
            border-radius: 13px;
            color: white;
            font-weight: 800;
            background: linear-gradient(135deg,#7c3aed,#5b21b6);
            cursor: pointer;
            margin-top: 8px;
        }

        .back {
            display: block;
            margin-top: 22px;
            color: #7c3aed;
            font-weight: 800;
            text-decoration: none;
        }

        .error {
            background: #fee2e2;
            color: #991b1b;
            padding: 13px;
            border-radius: 12px;
            margin-bottom: 18px;
            font-weight: 700;
        }

    </style>
</head>

<body>

    <div class="login-card">

        <div class="icon">🔐</div>

        <h1>{{ t.staff_login_title }}</h1>

        <p class="subtitle">
            {{ t.staff_login_text }}
        </p>

        {% if error %}
            <div class="error">
                {{ t.invalid_login }}
            </div>
        {% endif %}

        <form method="POST">

            <div class="field">
                <label>{{ t.username }}</label>

                <input
                    type="text"
                    name="username"
                    autocomplete="username"
                    required
                >
            </div>

            <div class="field">
                <label>{{ t.password }}</label>

                <input
                    type="password"
                    name="password"
                    autocomplete="current-password"
                    required
                >
            </div>

            <button type="submit">
                {{ t.sign_in }}
            </button>

        </form>

        <a class="back" href="{{ url_for('home') }}">
            ← {{ t.back_home }}
        </a>

    </div>

</body>

</html>
"""


# ---------------------------------------------------------
# STAFF DASHBOARD TEMPLATE
# ---------------------------------------------------------

STAFF_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{{ t.dashboard }}</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background: #faf8ff;
            color: #20152f;
        }

        .top {
            background: white;
            border-bottom: 1px solid #e7def5;
        }

        .top-inner {
            width: min(1100px, 92%);
            margin: auto;
            min-height: 75px;

            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }

        .brand {
            font-weight: 900;
        }

        .brand small {
            display: block;
            color: #7c3aed;
            margin-top: 3px;
        }

        .actions {
            display: flex;
            gap: 8px;
        }

        .button {
            border: 0;
            border-radius: 11px;
            padding: 10px 14px;
            font-weight: 800;
            text-decoration: none;
            cursor: pointer;
        }

        .home {
            background: #ede9fe;
            color: #5b21b6;
        }

        .logout {
            background: #7c3aed;
            color: white;
        }

        main {
            width: min(1100px, 92%);
            margin: auto;
            padding: 60px 0;
        }

        .heading {
            text-align: center;
            margin-bottom: 40px;
        }

        .heading h1 {
            font-size: clamp(34px, 5vw, 50px);
            margin: 0 0 12px;
        }

        .heading p {
            color: #6b6175;
            line-height: 1.7;
            max-width: 650px;
            margin: auto;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3,1fr);
            gap: 18px;
            margin-bottom: 35px;
        }

        .stat {
            background: white;
            border: 1px solid #e7def5;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
        }

        .stat-number {
            font-size: 34px;
            font-weight: 900;
            color: #7c3aed;
        }

        .stat-label {
            color: #6b6175;
            font-weight: 700;
            margin-top: 5px;
        }

        .requests {
            display: grid;
            gap: 17px;
        }

        .request-card {
            background: white;
            border: 1px solid #e7def5;
            border-radius: 20px;
            padding: 24px;
        }

        .request-card.handled {
            opacity: 0.7;
        }

        .request-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }

        .patient-name {
            font-size: 21px;
            font-weight: 900;
        }

        .badge {
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 12px;
            font-weight: 900;
        }

        .badge.pending {
            background: #ede9fe;
            color: #6d28d9;
        }

        .badge.handled {
            background: #dcfce7;
            color: #166534;
        }

        .details {
            display: grid;
            grid-template-columns: repeat(3,1fr);
            gap: 15px;
            margin-bottom: 15px;
            text-align: center;
        }

        .detail {
            background: #f5f3ff;
            border-radius: 13px;
            padding: 12px;
        }

        .detail strong {
            display: block;
            font-size: 11px;
            color: #7c3aed;
            margin-bottom: 4px;
        }

        .detail span {
            font-size: 13px;
            font-weight: 700;
        }

        .message {
            background: #f5f3ff;
            border-radius: 13px;
            padding: 16px;
            line-height: 1.6;
            margin-bottom: 15px;
        }

        .handle-form {
            text-align: center;
        }

        .handle {
            border: 0;
            background: #7c3aed;
            color: white;
            padding: 11px 18px;
            border-radius: 11px;
            font-weight: 800;
            cursor: pointer;
        }

        .empty {
            text-align: center;
            background: white;
            border: 1px solid #e7def5;
            border-radius: 22px;
            padding: 50px 20px;
            color: #6b6175;
        }

        .empty-icon {
            font-size: 40px;
            margin-bottom: 12px;
        }

        @media(max-width:700px) {

            .stats {
                grid-template-columns: 1fr;
            }

            .details {
                grid-template-columns: 1fr;
            }

            .top-inner {
                flex-direction: column;
                justify-content: center;
                padding: 15px 0;
            }

        }

    </style>

</head>

<body>

    <header class="top">

        <div class="top-inner">

            <div class="brand">
                Medina General Hospital
                <small>{{ t.staff }} • {{ t.dashboard }}</small>
            </div>

            <div class="actions">

                <a
                    class="button home"
                    href="{{ url_for('home') }}"
                >
                    {{ t.back_home }}
                </a>

                <a
                    class="button logout"
                    href="{{ url_for('staff_logout') }}"
                    onclick="sessionStorage.removeItem('staffLoggedIn');"
                >
                    {{ t.logout }}
                </a>

            </div>

        </div>

    </header>


    <main>

        <div class="heading">

            <h1>{{ t.dashboard }}</h1>

            <p>
                {{ t.dashboard_intro }}
            </p>

        </div>


        <div class="stats">

            <div class="stat">
                <div class="stat-number">
                    {{ pending_count }}
                </div>

                <div class="stat-label">
                    {{ t.pending }}
                </div>
            </div>

            <div class="stat">
                <div class="stat-number">
                    {{ handled_count }}
                </div>

                <div class="stat-label">
                    {{ t.handled }}
                </div>
            </div>

            <div class="stat">
                <div class="stat-number">
                    {{ requests|length }}
                </div>

                <div class="stat-label">
                    {{ t.all_requests }}
                </div>
            </div>

        </div>


        {% if requests %}

            <div class="requests">

                {% for item in requests|reverse %}

                    <div
                        class="request-card {% if item.status == 'handled' %}handled{% endif %}"
                    >

                        <div class="request-top">

                            <div class="patient-name">
                                👤 {{ item.name }}
                            </div>

                            {% if item.status == "pending" %}

                                <span class="badge pending">
                                    {{ t.pending_label }}
                                </span>

                            {% else %}

                                <span class="badge handled">
                                    {{ t.handled_label }}
                                </span>

                            {% endif %}

                        </div>


                        <div class="details">

                            <div class="detail">
                                <strong>{{ t.contact }}</strong>
                                <span>{{ item.contact }}</span>
                            </div>

                            <div class="detail">
                                <strong>{{ t.request }}</strong>
                                <span>{{ item.request_type }}</span>
                            </div>

                            <div class="detail">
                                <strong>{{ t.time }}</strong>
                                <span>{{ item.time }}</span>
                            </div>

                        </div>


                        <div class="message">
                            {{ item.message }}
                        </div>


                        {% if item.status == "pending" %}

                            <div class="handle-form">

                                <form
                                    method="POST"
                                    action="{{ url_for('mark_handled', request_id=item.id) }}"
                                >

                                    <button class="handle" type="submit">
                                        ✓ {{ t.mark_handled }}
                                    </button>

                                </form>

                            </div>

                        {% endif %}

                    </div>

                {% endfor %}

            </div>

        {% else %}

            <div class="empty">

                <div class="empty-icon">
                    📭
                </div>

                <strong>
                    {{ t.no_requests }}
                </strong>

            </div>

        {% endif %}

    </main>


    <script>

        /*
         * IMPORTANT:
         *
         * sessionStorage disappears when the browser tab/window
         * is closed.
         *
         * Therefore, if someone opens the staff dashboard again
         * after closing the website, they are automatically logged out.
         */

        if (sessionStorage.getItem("staffLoggedIn") !== "1") {

            fetch("{{ url_for('staff_logout') }}", {
                method: "GET",
                credentials: "same-origin"
            }).finally(function() {
                window.location.href = "{{ url_for('staff_login') }}";
            });

        }

    </script>

</body>

</html>
"""


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@app.route("/")
def home():
    success = request.args.get("success") == "1"
    error = request.args.get("error") == "1"

    return render_template_string(
        HOME_TEMPLATE,
        success=success,
        error=error
    )


@app.route("/set-language/<language>")
def set_language(language):

    if language not in TRANSLATIONS:
        language = "en"

    session["language"] = language

    # Keep the user on the main homepage.
    return redirect(url_for("home"))


# ---------------------------------------------------------
# ASSISTANCE FORM
# ---------------------------------------------------------

@app.route("/submit-assistance", methods=["POST"])
def submit_assistance():

    name = request.form.get("name", "").strip()
    contact = request.form.get("contact", "").strip()
    request_type = request.form.get("request_type", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not contact or not request_type or not message:
        return redirect(
            url_for("home", error="1") + "#assistance"
        )

    new_request = {
        "id": secrets.token_hex(8),
        "name": name,
        "contact": contact,
        "request_type": request_type,
        "message": message,
        "status": "pending",
        "time": datetime.now().strftime("%b %d, %Y • %I:%M %p")
    }

    assistance_requests.append(new_request)

    return redirect(
        url_for("home", success="1") + "#assistance"
    )


# ---------------------------------------------------------
# STAFF LOGIN
# ---------------------------------------------------------

@app.route("/staff", methods=["GET", "POST"])
def staff_login():

    # If already logged in on the server,
    # dashboard access is allowed.
    if session.get("staff_logged_in"):
        return redirect(url_for("staff_dashboard"))

    error = False

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            secrets.compare_digest(username, STAFF_USERNAME)
            and secrets.compare_digest(password, STAFF_PASSWORD)
        ):

            session.clear()

            session["staff_logged_in"] = True
            session["staff_username"] = username
            session["language"] = request.args.get(
                "lang",
                "en"
            )

            return redirect(url_for("staff_dashboard"))

        error = True

    return render_template_string(
        LOGIN_TEMPLATE,
        error=error
    )


# ---------------------------------------------------------
# STAFF DASHBOARD
# ---------------------------------------------------------

@app.route("/staff/dashboard")
@staff_required
def staff_dashboard():

    pending_count = sum(
        1 for item in assistance_requests
        if item["status"] == "pending"
    )

    handled_count = sum(
        1 for item in assistance_requests
        if item["status"] == "handled"
    )

    return render_template_string(
        STAFF_TEMPLATE,
        requests=assistance_requests,
        pending_count=pending_count,
        handled_count=handled_count
    )


# ---------------------------------------------------------
# MARK REQUEST AS HANDLED
# ---------------------------------------------------------

@app.route("/staff/handle/<request_id>", methods=["POST"])
@staff_required
def mark_handled(request_id):

    for item in assistance_requests:

        if item["id"] == request_id:
            item["status"] = "handled"
            break

    return redirect(url_for("staff_dashboard"))


# ---------------------------------------------------------
# STAFF LOGOUT
# ---------------------------------------------------------

@app.route("/staff/logout")
def staff_logout():

    session.clear()

    return redirect(url_for("staff_login"))


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


# ---------------------------------------------------------
# RUN LOCALLY
# ---------------------------------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
