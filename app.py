```python
from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dr. Bebie Queen Lucelle R. Tagupa - Licensed Physician and Psychiatrist">
    <title>Dr. Bebie Queen Lucelle R. Tagupa | Psychiatrist</title>

    <style>
        :root {
            --purple: #7c3aed;
            --purple-dark: #5b21b6;
            --purple-light: #a78bfa;
            --purple-soft: #efe7ff;

            --bg: #faf8ff;
            --bg2: #f2ecff;
            --card: #ffffff;

            --text: #21152d;
            --muted: #6f6479;

            --border: rgba(124, 58, 237, 0.14);
            --shadow: 0 20px 55px rgba(81, 45, 120, 0.12);
        }

        body.dark {
            --bg: #100917;
            --bg2: #1a1024;
            --card: #1e1429;

            --text: #f8f3ff;
            --muted: #c8bdd4;

            --border: rgba(167, 139, 250, 0.18);
            --shadow: 0 20px 55px rgba(0, 0, 0, 0.38);
        }

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
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            color: var(--text);
            background:
                radial-gradient(circle at 10% 5%,
                    rgba(124, 58, 237, 0.10),
                    transparent 28%
                ),
                radial-gradient(circle at 90% 20%,
                    rgba(167, 139, 250, 0.10),
                    transparent 28%
                ),
                var(--bg);

            line-height: 1.6;
            transition: 0.25s ease;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        button,
        select {
            font: inherit;
        }

        .container {
            width: min(1120px, 92%);
            margin: auto;
        }

        /* =========================
           HEADER
        ========================= */

        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;

            background: rgba(250, 248, 255, 0.84);
            backdrop-filter: blur(18px);

            border-bottom: 1px solid var(--border);
        }

        body.dark header {
            background: rgba(16, 9, 23, 0.84);
        }

        nav {
            min-height: 76px;

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo {
            width: 44px;
            height: 44px;

            display: grid;
            place-items: center;

            border-radius: 14px;

            color: white;

            background:
                linear-gradient(
                    135deg,
                    var(--purple),
                    var(--purple-dark)
                );

            box-shadow:
                0 10px 25px
                rgba(124, 58, 237, 0.25);
        }

        .brand small {
            display: block;

            color: var(--purple);

            font-size: 10px;
            font-weight: 900;

            text-transform: uppercase;
            letter-spacing: 1.4px;
        }

        .brand strong {
            display: block;
            font-size: 15px;
        }

        .nav-links {
            display: flex;
            gap: 24px;
        }

        .nav-links a {
            color: var(--muted);

            font-size: 14px;
            font-weight: 700;

            transition: 0.2s;
        }

        .nav-links a:hover {
            color: var(--purple);
        }

        .actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        #language {
            height: 40px;

            padding: 0 11px;

            border: 1px solid var(--border);
            border-radius: 12px;

            background: var(--card);
            color: var(--text);

            outline: none;
            cursor: pointer;
        }

        #themeButton {
            width: 40px;
            height: 40px;

            border: 1px solid var(--border);
            border-radius: 12px;

            background: var(--card);
            color: var(--text);

            cursor: pointer;
            font-size: 18px;
        }

        /* =========================
           HERO
        ========================= */

        .hero {
            padding: 145px 0 85px;
        }

        .hero-grid {
            display: grid;

            grid-template-columns:
                1.05fr
                0.95fr;

            gap: 65px;

            align-items: center;
        }

        .pill {
            display: inline-flex;

            padding: 8px 13px;

            margin-bottom: 20px;

            border-radius: 999px;

            background: var(--purple-soft);
            color: var(--purple-dark);

            font-size: 11px;
            font-weight: 900;

            text-transform: uppercase;
            letter-spacing: 1.1px;
        }

        body.dark .pill {
            color: #e0d2ff;
        }

        .hero h1 {
            font-size: clamp(43px, 6vw, 72px);

            line-height: 1.03;

            letter-spacing: -3px;

            margin-bottom: 22px;
        }

        .purple {
            color: var(--purple);
        }

        .hero-text {
            max-width: 640px;

            color: var(--muted);

            font-size: 18px;
            line-height: 1.8;

            margin-bottom: 30px;
        }

        .buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }

        .button {
            min-height: 50px;

            display: inline-flex;

            align-items: center;
            justify-content: center;

            gap: 8px;

            padding: 0 20px;

            border-radius: 14px;

            font-size: 14px;
            font-weight: 800;

            transition: 0.2s;
        }

        .primary {
            color: white;

            background:
                linear-gradient(
                    135deg,
                    var(--purple),
                    var(--purple-dark)
                );

            box-shadow:
                0 14px 30px
                rgba(124, 58, 237, 0.24);
        }

        .primary:hover {
            transform: translateY(-3px);
        }

        .secondary {
            color: var(--text);

            background: var(--card);

            border: 1px solid var(--border);
        }

        .secondary:hover {
            transform: translateY(-3px);
            border-color: var(--purple-light);
        }

        /* =========================
           PHOTO
        ========================= */

        .photo-area {
            position: relative;

            display: flex;
            justify-content: center;
        }

        .photo-glow {
            position: absolute;

            width: 390px;
            height: 390px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(124, 58, 237, 0.30),
                    transparent 68%
                );
        }

        .photo-card {
            position: relative;

            width: min(420px, 100%);

            padding: 11px;

            border-radius: 32px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #eee7ff
                );

            box-shadow: var(--shadow);

            transform: rotate(1deg);
        }

        body.dark .photo-card {
            background:
                linear-gradient(
                    145deg,
                    #3a284d,
                    #1d1326
                );
        }

        .doctor-photo {
            display: block;

            width: 100%;
            aspect-ratio: 4 / 5;

            object-fit: cover;
            object-position: center;

            border-radius: 23px;

            background: var(--purple-soft);
        }

        .photo-badge {
            position: absolute;

            left: -24px;
            bottom: 27px;

            padding: 15px 17px;

            border-radius: 17px;

            background: var(--card);

            border: 1px solid var(--border);

            box-shadow: var(--shadow);
        }

        .photo-badge strong {
            display: block;
            font-size: 13px;
        }

        .photo-badge span {
            display: block;

            margin-top: 3px;

            color: var(--muted);

            font-size: 11px;
        }

        /* =========================
           QUICK CARDS
        ========================= */

        .quick {
            margin-top: -18px;

            position: relative;
            z-index: 2;
        }

        .quick-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }

        .quick-card {
            padding: 24px;

            border-radius: 20px;

            background: var(--card);

            border: 1px solid var(--border);

            box-shadow: var(--shadow);
        }

        .quick-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .quick-card h3 {
            font-size: 16px;
            margin-bottom: 5px;
        }

        .quick-card p {
            color: var(--muted);
            font-size: 13px;
        }

        /* =========================
           SECTIONS
        ========================= */

        section {
            padding: 100px 0;
        }

        .section-alt {
            background: var(--bg2);
        }

        .section-heading {
            max-width: 730px;

            margin:
                0 auto 48px;

            text-align: center;
        }

        .kicker {
            color: var(--purple);

            font-size: 11px;
            font-weight: 900;

            letter-spacing: 2px;
            text-transform: uppercase;

            margin-bottom: 10px;
        }

        .section-heading h2 {
            font-size:
                clamp(
                    32px,
                    5vw,
                    48px
                );

            line-height: 1.1;

            letter-spacing: -1.8px;

            margin-bottom: 14px;
        }

        .section-heading p {
            color: var(--muted);
        }

        /* =========================
           ABOUT
        ========================= */

        .about-grid {
            display: grid;

            grid-template-columns:
                0.78fr
                1.22fr;

            gap: 60px;

            align-items: center;
        }

        .quote-box {
            padding: 35px;

            background: var(--card);

            border: 1px solid var(--border);

            border-radius: 28px;

            box-shadow: var(--shadow);

            font-size: 29px;
            font-weight: 850;

            line-height: 1.3;
        }

        .quote-box span {
            color: var(--purple);
        }

        .about-text h2 {
            font-size: 41px;

            letter-spacing: -1.5px;

            margin-bottom: 18px;
        }

        .about-text p {
            color: var(--muted);

            margin-bottom: 14px;
        }

        /* =========================
           CREDENTIALS
        ========================= */

        .credentials {
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 16px;
        }

        .credential {
            padding: 23px;

            background: var(--card);

            border: 1px solid var(--border);

            border-radius: 19px;
        }

        .credential-number {
            color: var(--purple);

            font-size: 11px;
            font-weight: 900;

            letter-spacing: 1px;
        }

        .credential h3 {
            margin:
                7px 0 3px;

            font-size: 16px;
        }

        .credential p {
            color: var(--muted);
            font-size: 13px;
        }

        /* =========================
           SERVICES
        ========================= */

        .services-grid {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 20px;
        }

        .service {
            position: relative;

            overflow: hidden;

            padding: 30px;

            background: var(--card);

            border: 1px solid var(--border);

            border-radius: 24px;

            box-shadow: var(--shadow);

            transition: 0.25s;
        }

        .service:hover {
            transform: translateY(-5px);
        }

        .service::before {
            content: "";

            position: absolute;

            top: 0;
            left: 0;

            width: 100%;
            height: 4px;

            background:
                linear-gradient(
                    90deg,
                    var(--purple),
                    var(--purple-light)
                );
        }

        .service-icon {
            width: 54px;
            height: 54px;

            display: grid;
            place-items: center;

            margin-bottom: 18px;

            border-radius: 15px;

            background: var(--bg2);

            font-size: 24px;
        }

        .service h3 {
            margin-bottom: 9px;
            font-size: 19px;
        }

        .service p {
            color: var(--muted);
            font-size: 14px;
        }

        /* =========================
           JOURNEY
        ========================= */

        .journey {
            color: white;

            background:
                linear-gradient(
                    135deg,
                    var(--purple-dark),
                    var(--purple)
                );
        }

        .journey .section-heading p {
            color: rgba(255,255,255,.78);
        }

        .journey-grid {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 20px;
        }

        .step {
            padding: 29px;

            background:
                rgba(255,255,255,.09);

            border:
                1px solid
                rgba(255,255,255,.15);

            border-radius: 22px;
        }

        .step-number {
            width: 43px;
            height: 43px;

            display: grid;
            place-items: center;

            margin-bottom: 15px;

            border-radius: 50%;

            background:
                rgba(255,255,255,.14);

            font-weight: 900;
        }

        .step h3 {
            margin-bottom: 7px;
        }

        .step p {
            color: rgba(255,255,255,.76);
            font-size: 14px;
        }

        /* =========================
           CLINIC
        ========================= */

        .clinic-grid {
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 20px;
        }

        .clinic {
            padding: 32px;

            background: var(--card);

            border: 1px solid var(--border);

            border-radius: 24px;

            box-shadow: var(--shadow);
        }

        .clinic h3 {
            font-size: 21px;
            margin-bottom: 14px;
        }

        .clinic-row {
            display: flex;

            align-items: flex-start;

            gap: 13px;

            padding: 15px 0;

            border-bottom:
                1px solid
                var(--border);
        }

        .clinic-row:last-child {
            border-bottom: none;
        }

        .clinic-icon {
            width: 42px;
            height: 42px;

            flex: none;

            display: grid;
            place-items: center;

            border-radius: 12px;

            background: var(--bg2);
        }

        .clinic-row strong {
            display: block;
            font-size: 14px;
        }

        .clinic-row span {
            color: var(--muted);
            font-size: 14px;
        }

        /* =========================
           CTA
        ========================= */

        .cta {
            padding: 80px 0;
        }

        .cta-box {
            padding: 63px 30px;

            text-align: center;

            color: white;

            border-radius: 31px;

            background:
                linear-gradient(
                    135deg,
                    #351166,
                    var(--purple-dark)
                );

            box-shadow:
                0 24px 65px
                rgba(91,33,182,.25);
        }

        .cta-box h2 {
            font-size:
                clamp(
                    30px,
                    5vw,
                    48px
                );

            line-height: 1.1;

            letter-spacing: -1.5px;

            margin-bottom: 13px;
        }

        .cta-box p {
            max-width: 620px;

            margin:
                0 auto 26px;

            color:
                rgba(
                    255,
                    255,
                    255,
                    .78
                );
        }

        .cta-button {
            display: inline-flex;

            align-items: center;
            justify-content: center;

            min-height: 50px;

            padding:
                0 21px;

            border-radius: 14px;

            background: white;

            color: var(--purple-dark);

            font-size: 14px;
            font-weight: 900;
        }

        /* =========================
           FOOTER
        ========================= */

        footer {
            padding: 34px 0;

            background: var(--bg2);

            border-top:
                1px solid
                var(--border);
        }

        .footer-row {
            display: flex;

            justify-content: space-between;
            align-items: center;

            gap: 20px;
        }

        .footer-row strong {
            font-size: 14px;
        }

        .footer-row span {
            color: var(--muted);
            font-size: 12px;
        }

        /* =========================
           LANGUAGE
        ========================= */

        .lang {
            display: none;
        }

        .lang.active {
            display: block;
        }

        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 900px) {

            .nav-links {
                display: none;
            }

            .hero-grid,
            .about-grid,
            .clinic-grid {
                grid-template-columns: 1fr;
            }

            .photo-area {
                order: -1;
            }

            .quick-grid,
            .services-grid,
            .journey-grid {
                grid-template-columns: 1fr;
            }

            .credentials {
                grid-template-columns: 1fr;
            }

            .quick {
                margin-top: 0;
            }

            .about-text h2 {
                font-size: 34px;
            }

            .photo-badge {
                left: 8px;
            }

            .footer-row {
                flex-direction: column;
                text-align: center;
            }
        }

        @media (max-width: 560px) {

            .brand small,
            .brand strong {
                display: none;
            }

            .hero {
                padding-top: 120px;
            }

            .hero h1 {
                font-size: 43px;
                letter-spacing: -2px;
            }

            .hero-text {
                font-size: 16px;
            }

            .buttons {
                flex-direction: column;
            }

            .button {
                width: 100%;
            }

            section {
                padding: 75px 0;
            }
        }
    </style>
</head>

<body>

<header>
    <div class="container">

        <nav>

            <a class="brand" href="#home">

                <div class="logo">
                    ♡
                </div>

                <div>
                    <small>
                        Psychiatry & Mental Wellness
                    </small>

                    <strong>
                        Dr. Bebie Tagupa
                    </strong>
                </div>

            </a>

            <div class="nav-links">
                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#services">Services</a>
                <a href="#clinic">Clinic</a>
            </div>

            <div class="actions">

                <select
                    id="language"
                    aria-label="Choose language"
                    onchange="changeLanguage()"
                >
                    <option value="en">English</option>
                    <option value="fil">Filipino</option>
                    <option value="ceb">Visaya</option>
                </select>

                <button
                    id="themeButton"
                    type="button"
                    onclick="toggleTheme()"
                    aria-label="Toggle dark and light mode"
                >
                    🌙
                </button>

            </div>

        </nav>

    </div>
</header>


<main>

<!-- ================= HERO ================= -->

<section class="hero" id="home">

    <div class="container">

        <div class="hero-grid">

            <div>

                <div class="pill">
                    ✦ Licensed Physician & Psychiatrist
                </div>


                <div class="lang active" data-lang="en">

                    <h1>
                        Your mind deserves
                        <span class="purple">
                            care.
                        </span>
                    </h1>

                    <p class="hero-text">
                        Compassionate, patient-centered psychiatric
                        care focused on helping you understand your
                        mental well-being, find support, and move
                        toward a healthier and more fulfilling life.
                    </p>

                    <div class="buttons">

                        <a
                            class="button primary"
                            href="#clinic"
                        >
                            📅 View Clinic Schedule
                        </a>

                        <a
                            class="button secondary"
                            href="#about"
                        >
                            Meet Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <div class="lang" data-lang="fil">

                    <h1>
                        Ang iyong isip ay
                        <span class="purple">
                            mahalaga.
                        </span>
                    </h1>

                    <p class="hero-text">
                        Maalagang psychiatric care na nakatuon sa
                        bawat pasyente. Layunin naming tulungan kang
                        maunawaan ang iyong mental well-being at
                        magkaroon ng mas malusog at makabuluhang buhay.
                    </p>

                    <div class="buttons">

                        <a
                            class="button primary"
                            href="#clinic"
                        >
                            📅 Tingnan ang Schedule
                        </a>

                        <a
                            class="button secondary"
                            href="#about"
                        >
                            Kilalanin si Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <div class="lang" data-lang="ceb">

                    <h1>
                        Importante ang imong
                        <span class="purple">
                            hunahuna.
                        </span>
                    </h1>

                    <p class="hero-text">
                        Mainiton ug maloloy-on nga psychiatric care
                        nga nakasentro sa panginahanglan sa matag
                        pasyente. Ania kami aron motabang kanimo sa
                        pag-atiman sa imong mental well-being ug kinabuhi.
                    </p>

                    <div class="buttons">

                        <a
                            class="button primary"
                            href="#clinic"
                        >
                            📅 Tan-awa ang Schedule
                        </a>

                        <a
                            class="button secondary"
                            href="#about"
                        >
                            Ilaila si Dr. Tagupa →
                        </a>

                    </div>

                </div>

            </div>


            <div class="photo-area">

                <div class="photo-glow"></div>

                <div class="photo-card">

                    <img
                        class="doctor-photo"
                        src="/static/image0%20%282%29.jpeg"
                        alt="Dr. Bebie Queen Lucelle R. Tagupa"
                    >

                    <div class="photo-badge">

                        <strong>
                            Dr. Bebie Queen Lucelle R. Tagupa
                        </strong>

                        <span>
                            Licensed Physician • Psychiatrist
                        </span>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- ================= QUICK ================= -->

<section class="quick">

    <div class="container">

        <div class="quick-grid">

            <div class="quick-card">

                <div class="quick-icon">
                    🩺
                </div>

                <h3>
                    Licensed Physician
                </h3>

                <p>
                    Medical doctor committed to compassionate,
                    patient-centered care.
                </p>

            </div>


            <div class="quick-card">

                <div class="quick-icon">
                    🧠
                </div>

                <h3>
                    Psychiatry
                </h3>

                <p>
                    Specialized psychiatric evaluation and treatment.
                </p>

            </div>


            <div class="quick-card">

                <div class="quick-icon">
                    💜
                </div>

                <h3>
                    Patient-Centered
                </h3>

                <p>
                    Your story, concerns, and well-being come first.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- ================= ABOUT ================= -->

<section
    class="section-alt"
    id="about"
>

    <div class="container">

        <div class="about-grid">

            <div class="quote-box">

                “Mental health care begins with
                <span>
                    being heard.
                </span>”

            </div>


            <div class="about-text">

                <div class="kicker">
                    About the Doctor
                </div>


                <div
                    class="lang active"
                    data-lang="en"
                >

                    <h2>
                        Meet Dr. Tagupa
                    </h2>

                    <p>
                        Dr. Bebie Queen Lucelle R. Tagupa is a licensed
                        physician and psychiatrist dedicated to providing
                        compassionate, patient-centered mental health care.
                    </p>

                    <p>
                        She earned her Bachelor’s degree in Medical
                        Technology from Velez College and is also a
                        licensed Medical Technologist.
                    </p>

                    <p>
                        She proceeded to study Medicine at Xavier
                        University – Ateneo de Cagayan.
                    </p>

                    <p>
                        She completed her post-graduate internship at
                        Davao Doctors Hospital and finished her residency
                        training in Psychiatry at the Southern Philippines
                        Medical Center – Institute of Psychiatry and
                        Behavioral Medicine.
                    </p>

                    <p>
                        During her final year of training, she served as
                        Chief Resident and was awarded Most Outstanding
                        Resident in Psychiatry during her graduation.
                    </p>

                </div>


                <div
                    class="lang"
                    data-lang="fil"
                >

                    <h2>
                        Kilalanin si Dr. Tagupa
                    </h2>

                    <p>
                        Si Dr. Bebie Queen Lucelle R. Tagupa ay isang
                        licensed physician at psychiatrist na nakatuon
                        sa mahabagin at patient-centered na pangangalaga
                        sa mental health.
                    </p>

                    <p>
                        Natapos niya ang kanyang Bachelor’s degree sa
                        Medical Technology sa Velez College at isa rin
                        siyang licensed Medical Technologist.
                    </p>

                    <p>
                        Nagpatuloy siya sa pag-aaral ng Medicine sa
                        Xavier University – Ateneo de Cagayan.
                    </p>

                    <p>
                        Nakumpleto niya ang post-graduate internship
                        sa Davao Doctors Hospital at residency training
                        sa Psychiatry sa Southern Philippines Medical
                        Center – Institute of Psychiatry and Behavioral
                        Medicine.
                    </p>

                    <p>
                        Sa kanyang huling taon ng training, nagsilbi siya
                        bilang Chief Resident at ginawaran bilang
                        Most Outstanding Resident in Psychiatry.
                    </p>

                </div>


                <div
                    class="lang"
                    data-lang="ceb"
                >

                    <h2>
                        Ilaila si Dr. Tagupa
                    </h2>

                    <p>
                        Si Dr. Bebie Queen Lucelle R. Tagupa usa ka
                        licensed physician ug psychiatrist nga naghatag
                        og maloloy-on ug patient-centered nga mental
                        health care.
                    </p>

                    <p>
                        Nakakuha siya sa iyang Bachelor’s degree sa
                        Medical Technology gikan sa Velez College ug
                        usa usab siya ka licensed Medical Technologist.
                    </p>

                    <p>
                        Nagpadayon siya sa pagtuon og Medicine sa
                        Xavier University – Ateneo de Cagayan.
                    </p>

                    <p>
                        Nakompleto niya ang post-graduate internship
                        sa Davao Doctors Hospital ug residency training
                        sa Psychiatry sa Southern Philippines Medical
                        Center – Institute of Psychiatry and Behavioral
                        Medicine.
                    </p>

                    <p>
                        Sa iyang katapusang tuig sa training, nagsilbi
                        siya isip Chief Resident ug nadawat ang award
                        nga Most Outstanding Resident in Psychiatry.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- ================= CREDENTIALS ================= -->

<section>

    <div class="container">

        <div class="section-heading">

            <div class="kicker">
                Education & Training
            </div>

            <h2>
                A journey built on dedication.
            </h2>

            <p>
                A strong academic and clinical foundation supporting
                compassionate psychiatric care.
            </p>

        </div>


        <div class="credentials">

            <div class="credential">

                <div class="credential-number">
                    01
                </div>

                <h3>
                    Bachelor of Medical Technology
                </h3>

                <p>
                    Velez College
                </p>

            </div>


            <div class="credential">

                <div class="credential-number">
                    02
                </div>

                <h3>
                    Licensed Medical Technologist
                </h3>

                <p>
                    Professional medical laboratory background.
                </p>

            </div>


            <div class="credential">

                <div class="credential-number">
                    03
                </div>

                <h3>
                    Doctor of Medicine
                </h3>

                <p>
                    Xavier University – Ateneo de Cagayan
                </p>

            </div>


            <div class="credential">

                <div class="credential-number">
                    04
                </div>

                <h3>
                    Post-Graduate Internship
                </h3>

                <p>
                    Davao Doctors Hospital
                </p>

            </div>


            <div class="credential">

                <div class="credential-number">
                    05
                </div>

                <h3>
                    Psychiatry Residency
                </h3>

                <p>
                    Southern Philippines Medical Center –
                    Institute of Psychiatry and Behavioral Medicine
                </p>

            </div>


            <div class="credential">

                <div class="credential-number">
                    06
                </div>

                <h3>
                    Chief Resident
                </h3>

                <p>
                    Served as Chief Resident during her final year
                    of Psychiatry residency.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- ================= SERVICES ================= -->

<section
    class="section-alt"
    id="services"
>

    <div class="container">

        <div class="section-heading">

            <div class="kicker">
                Mental Health Care
            </div>

            <h2>
                Care that starts with you.
            </h2>

            <p>
                Psychiatric evaluation and treatment for a wide range
                of mental health conditions.
            </p>

        </div>


        <div class="services-grid">

            <div class="service">

                <div class="service-icon">
                    🧠
                </div>

                <h3>
                    Psychiatric Evaluation
                </h3>

                <p>
                    Comprehensive assessment to better understand
                    mental health concerns and identify appropriate
                    treatment options.
                </p>

            </div>


            <div class="service">

                <div class="service-icon">
                    💬
                </div>

                <h3>
                    Mental Health Consultation
                </h3>

                <p>
                    A safe and respectful space to discuss concerns,
                    emotions, thoughts, behavior, and overall
                    mental well-being.
                </p>

            </div>


            <div class="service">

                <div class="service-icon">
                    🌱
                </div>

                <h3>
                    Treatment & Follow-Up
                </h3>

                <p>
                    Patient-centered treatment and follow-up based
                    on individual needs, goals, and progress.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- ================= JOURNEY ================= -->

<section class="journey">

    <div class="container">

        <div class="section-heading">

            <div
                class="kicker"
                style="color:#e1d3ff"
            >
                Your Care Journey
            </div>

            <h2>
                You don't have to figure it out alone.
            </h2>

            <p>
                Taking care of your mental health is a step-by-step
                journey. Every step matters.
            </p>

        </div>


        <div class="journey-grid">

            <div class="step">

                <div class="step-number">
                    1
                </div>

                <h3>
                    Be Heard
                </h3>

                <p>
                    Share your concerns in a respectful and
                    supportive environment.
                </p>

            </div>


            <div class="step">

                <div class="step-number">
                    2
                </div>

                <h3>
                    Understand
                </h3>

                <p>
                    Work toward understanding your mental health
                    and individual needs.
                </p>

            </div>


            <div class="step">

                <div class="step-number">
                    3
                </div>

                <h3>
                    Move Forward
                </h3>

                <p>
                    Develop an appropriate treatment plan and
                    continue toward better well-being.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- ================= CLINIC ================= -->

<section id="clinic">

    <div class="container">

        <div class="section-heading">

            <div class="kicker">
                Clinic Information
            </div>

            <h2>
                Visit the clinic.
            </h2>

            <p>
                Find the clinic location and consultation schedule below.
            </p>

        </div>


        <div class="clinic-grid">

            <div class="clinic">

                <h3>
                    📍 Clinic
                </h3>

                <div class="clinic-row">

                    <div class="clinic-icon">
                        🏥
                    </div>

                    <div>

                        <strong>
                            Hospital
                        </strong>

                        <span>
                            Medina General Hospital
                        </span>

                    </div>

                </div>


                <div class="clinic-row">

                    <div class="clinic-icon">
                        🚪
                    </div>

                    <div>

                        <strong>
                            Location
                        </strong>

                        <span>
                            OPD Door 2
                        </span>

                    </div>

                </div>

            </div>


            <div class="clinic">

                <h3>
                    🕘 Consultation Schedule
                </h3>

                <div class="clinic-row">

                    <div class="clinic-icon">
                        📅
                    </div>

                    <div>

                        <strong>
                            Days
                        </strong>

                        <span>
                            Tuesday • Thursday • Saturday
                        </span>

                    </div>

                </div>


                <div class="clinic-row">

                    <div class="clinic-icon">
                        ⏰
                    </div>

                    <div>

                        <strong>
                            Time
                        </strong>

                        <span>
                            9:00 AM – 4:00 PM
                        </span>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- ================= CTA ================= -->

<section class="cta">

    <div class="container">

        <div class="cta-box">

            <h2>
                Your mental well-being matters.
            </h2>

            <p>
                Taking the first step toward better mental health
                can be difficult. You don't have to take that step alone.
            </p>

            <a
                href="#clinic"
                class="cta-button"
            >
                View Clinic Schedule →
            </a>

        </div>

    </div>

</section>

</main>


<!-- ================= FOOTER ================= -->

<footer>

    <div class="container">

        <div class="footer-row">

            <div>
                <strong>
                    Dr. Bebie Queen Lucelle R. Tagupa
                </strong>

                <br>

                <span>
                    Licensed Physician • Psychiatrist
                </span>
            </div>

            <span>
                © 2026 Dr. Bebie Tagupa. All rights reserved.
            </span>

        </div>

    </div>

</footer>


<script>

    function changeLanguage() {

        const selected =
            document.getElementById("language").value;

        document
            .querySelectorAll(".lang")
            .forEach(function(element) {

                element.classList.toggle(
                    "active",
                    element.dataset.lang === selected
                );

            });

        localStorage.setItem(
            "language",
            selected
        );
    }


    function toggleTheme() {

        document.body.classList.toggle("dark");

        const isDark =
            document.body.classList.contains("dark");

        localStorage.setItem(
            "dark",
            isDark ? "1" : "0"
        );

        document.getElementById(
            "themeButton"
        ).textContent =
            isDark ? "☀️" : "🌙";
    }


    document.addEventListener(
        "DOMContentLoaded",
        function() {

            const savedLanguage =
                localStorage.getItem("language") || "en";

            document.getElementById(
                "language"
            ).value = savedLanguage;

            changeLanguage();


            const savedDark =
                localStorage.getItem("dark");

            if (savedDark === "1") {
                document.body.classList.add("dark");
            }


            document.getElementById(
                "themeButton"
            ).textContent =
                document.body.classList.contains("dark")
                ? "☀️"
                : "🌙";

        }
    );

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
```
