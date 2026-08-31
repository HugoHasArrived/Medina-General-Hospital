from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Dr. Bebie Queen Lucelle R. Tagupa | Psychiatrist</title>

    <meta
        name="description"
        content="Dr. Bebie Queen Lucelle R. Tagupa — Licensed Physician and Psychiatrist. Compassionate, patient-centered psychiatric care."
    >

    <style>

        /* =========================================================
           GLOBAL
        ========================================================= */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        :root {
            --purple: #7c3aed;
            --purple-dark: #5b21b6;
            --purple-light: #a78bfa;
            --purple-soft: #ede9fe;

            --bg: #faf8ff;
            --bg-secondary: #f3efff;
            --card: rgba(255,255,255,0.88);

            --text: #211536;
            --text-light: #675a78;
            --border: rgba(124,58,237,0.15);

            --shadow: 0 20px 60px rgba(79, 38, 126, 0.13);
        }

        body.dark {
            --bg: #100b18;
            --bg-secondary: #181021;
            --card: rgba(30,20,42,0.90);

            --text: #f8f5ff;
            --text-light: #c5b9d4;
            --border: rgba(167,139,250,0.18);

            --shadow: 0 20px 60px rgba(0,0,0,0.35);
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

            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(124,58,237,0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 30%,
                    rgba(167,139,250,0.12),
                    transparent 28%
                ),
                var(--bg);

            color: var(--text);
            min-height: 100vh;
            transition: background .3s ease, color .3s ease;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        button {
            font-family: inherit;
        }

        .container {
            width: min(1150px, 92%);
            margin: auto;
        }


        /* =========================================================
           NAVBAR
        ========================================================= */

        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;

            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);

            background: rgba(250,248,255,0.78);
            border-bottom: 1px solid var(--border);
        }

        body.dark header {
            background: rgba(16,11,24,0.80);
        }

        nav {
            min-height: 78px;

            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;

            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .brand-icon {
            width: 45px;
            height: 45px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 14px;

            background: linear-gradient(
                135deg,
                var(--purple),
                var(--purple-dark)
            );

            color: white;
            font-size: 21px;

            box-shadow:
                0 10px 25px rgba(124,58,237,.28);
        }

        .brand-text span {
            display: block;
            font-size: 11px;
            color: var(--purple);
            letter-spacing: 1.8px;
            text-transform: uppercase;
        }

        .brand-text strong {
            display: block;
            font-size: 16px;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 28px;
        }

        .nav-links a {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-light);
            transition: .2s;
        }

        .nav-links a:hover {
            color: var(--purple);
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 9px;
        }

        .language-select,
        .theme-button {
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);

            border-radius: 12px;
            padding: 9px 11px;

            cursor: pointer;
            font-weight: 600;
        }

        .language-select {
            outline: none;
        }

        .theme-button {
            width: 42px;
            height: 42px;
            padding: 0;
            font-size: 18px;
        }


        /* =========================================================
           HERO
        ========================================================= */

        .hero {
            padding: 150px 0 90px;
            min-height: 760px;

            display: flex;
            align-items: center;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.05fr .95fr;
            gap: 65px;
            align-items: center;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;

            padding: 8px 13px;
            margin-bottom: 20px;

            background: var(--purple-soft);
            color: var(--purple-dark);

            border-radius: 999px;

            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        body.dark .eyebrow {
            color: #d8c7ff;
            background: rgba(124,58,237,.20);
        }

        .hero h1 {
            font-size: clamp(42px, 6vw, 72px);
            line-height: 1.03;
            letter-spacing: -3px;

            margin-bottom: 23px;
        }

        .hero h1 .purple {
            color: var(--purple);
        }

        .hero-description {
            max-width: 640px;

            color: var(--text-light);
            font-size: 18px;
            line-height: 1.8;

            margin-bottom: 32px;
        }

        .hero-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 13px;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 9px;

            min-height: 50px;
            padding: 0 21px;

            border-radius: 14px;

            font-weight: 800;
            font-size: 14px;

            cursor: pointer;
            transition: .25s;
        }

        .button-primary {
            color: white;

            background:
                linear-gradient(
                    135deg,
                    var(--purple),
                    var(--purple-dark)
                );

            box-shadow:
                0 14px 30px rgba(124,58,237,.25);
        }

        .button-primary:hover {
            transform: translateY(-3px);
            box-shadow:
                0 18px 38px rgba(124,58,237,.35);
        }

        .button-secondary {
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
        }

        .button-secondary:hover {
            border-color: var(--purple-light);
            transform: translateY(-3px);
        }


        /* =========================================================
           DOCTOR IMAGE
        ========================================================= */

        .doctor-wrap {
            position: relative;
            display: flex;
            justify-content: center;
        }

        .doctor-glow {
            position: absolute;
            width: 360px;
            height: 360px;

            background:
                radial-gradient(
                    circle,
                    rgba(124,58,237,.30),
                    transparent 65%
                );

            filter: blur(5px);
        }

        .doctor-card {
            position: relative;
            width: min(420px, 100%);

            border-radius: 32px;
            padding: 12px;

            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,.9),
                    rgba(237,233,254,.7)
                );

            box-shadow: var(--shadow);

            transform: rotate(1deg);
        }

        body.dark .doctor-card {
            background:
                linear-gradient(
                    145deg,
                    rgba(55,38,75,.9),
                    rgba(30,20,42,.9)
                );
        }

        .doctor-photo {
            width: 100%;
            aspect-ratio: 4 / 5;

            object-fit: cover;
            object-position: center;

            border-radius: 23px;
            display: block;

            background: var(--purple-soft);
        }

        .doctor-badge {
            position: absolute;
            bottom: 30px;
            left: -28px;

            padding: 17px 20px;

            background: var(--card);
            border: 1px solid var(--border);

            border-radius: 18px;

            box-shadow: var(--shadow);

            transform: rotate(-1deg);
        }

        .doctor-badge strong {
            display: block;
            font-size: 14px;
        }

        .doctor-badge span {
            display: block;
            margin-top: 4px;

            color: var(--text-light);
            font-size: 12px;
        }


        /* =========================================================
           QUICK INFO
        ========================================================= */

        .quick-info {
            margin-top: -25px;
            position: relative;
            z-index: 2;
        }

        .quick-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }

        .quick-card {
            padding: 25px;

            border: 1px solid var(--border);
            background: var(--card);

            border-radius: 20px;

            box-shadow: var(--shadow);
        }

        .quick-icon {
            font-size: 25px;
            margin-bottom: 13px;
        }

        .quick-card h3 {
            font-size: 16px;
            margin-bottom: 6px;
        }

        .quick-card p {
            color: var(--text-light);
            font-size: 13px;
            line-height: 1.6;
        }


        /* =========================================================
           SECTIONS
        ========================================================= */

        section {
            padding: 105px 0;
        }

        .section-heading {
            text-align: center;
            max-width: 720px;
            margin: 0 auto 55px;
        }

        .section-heading .small-title {
            color: var(--purple);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 900;
            font-size: 12px;
            margin-bottom: 12px;
        }

        .section-heading h2 {
            font-size: clamp(32px, 5vw, 48px);
            letter-spacing: -1.8px;
            margin-bottom: 14px;
        }

        .section-heading p {
            color: var(--text-light);
            line-height: 1.8;
        }


        /* =========================================================
           ABOUT
        ========================================================= */

        .about {
            background: var(--bg-secondary);
        }

        .about-grid {
            display: grid;
            grid-template-columns: .8fr 1.2fr;
            gap: 60px;
            align-items: center;
        }

        .about-card {
            padding: 35px;

            background: var(--card);
            border: 1px solid var(--border);

            border-radius: 28px;
            box-shadow: var(--shadow);
        }

        .about-card .quote {
            font-size: 29px;
            line-height: 1.3;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .about-card .quote span {
            color: var(--purple);
        }

        .about-text h2 {
            font-size: 42px;
            letter-spacing: -1.5px;
            margin-bottom: 20px;
        }

        .about-text p {
            color: var(--text-light);
            line-height: 1.9;
            margin-bottom: 17px;
        }


        /* =========================================================
           CREDENTIALS
        ========================================================= */

        .credentials {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
        }

        .credential {
            padding: 23px;

            background: var(--card);
            border: 1px solid var(--border);

            border-radius: 20px;
        }

        .credential-number {
            color: var(--purple);
            font-weight: 900;
            font-size: 12px;
            letter-spacing: 1px;
        }

        .credential h3 {
            margin: 8px 0;
            font-size: 16px;
        }

        .credential p {
            margin: 0;
            font-size: 13px;
            line-height: 1.65;
        }


        /* =========================================================
           SERVICES
        ========================================================= */

        .services-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .service-card {
            position: relative;
            overflow: hidden;

            padding: 30px;

            border: 1px solid var(--border);
            background: var(--card);

            border-radius: 24px;
            box-shadow: var(--shadow);

            transition: .25s;
        }

        .service-card::before {
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

        .service-card:hover {
            transform: translateY(-6px);
        }

        .service-icon {
            width: 54px;
            height: 54px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 16px;

            background: var(--purple-soft);
            font-size: 25px;

            margin-bottom: 20px;
        }

        body.dark .service-icon {
            background: rgba(124,58,237,.20);
        }

        .service-card h3 {
            margin-bottom: 10px;
            font-size: 19px;
        }

        .service-card p {
            color: var(--text-light);
            line-height: 1.75;
            font-size: 14px;
        }


        /* =========================================================
           JOURNEY
        ========================================================= */

        .journey {
            background:
                linear-gradient(
                    135deg,
                    var(--purple-dark),
                    var(--purple)
                );

            color: white;
        }

        .journey .section-heading p {
            color: rgba(255,255,255,.78);
        }

        .journey .small-title {
            color: #ddd0ff;
        }

        .journey-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .journey-step {
            padding: 30px;

            background: rgba(255,255,255,.10);
            border: 1px solid rgba(255,255,255,.16);

            border-radius: 23px;
            backdrop-filter: blur(10px);
        }

        .journey-step span {
            display: inline-flex;

            width: 42px;
            height: 42px;

            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background: rgba(255,255,255,.15);
            font-weight: 900;

            margin-bottom: 17px;
        }

        .journey-step h3 {
            margin-bottom: 9px;
        }

        .journey-step p {
            color: rgba(255,255,255,.75);
            line-height: 1.7;
            font-size: 14px;
        }


        /* =========================================================
           CLINIC
        ========================================================= */

        .clinic-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 22px;
        }

        .clinic-card {
            padding: 35px;

            background: var(--card);
            border: 1px solid var(--border);

            border-radius: 26px;
            box-shadow: var(--shadow);
        }

        .clinic-card h3 {
            font-size: 22px;
            margin-bottom: 18px;
        }

        .clinic-row {
            display: flex;
            gap: 15px;
            align-items: flex-start;

            padding: 17px 0;

            border-bottom: 1px solid var(--border);
        }

        .clinic-row:last-child {
            border-bottom: 0;
        }

        .clinic-row-icon {
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background: var(--purple-soft);

            flex-shrink: 0;
        }

        body.dark .clinic-row-icon {
            background: rgba(124,58,237,.20);
        }

        .clinic-row strong {
            display: block;
            font-size: 14px;
            margin-bottom: 4px;
        }

        .clinic-row p {
            color: var(--text-light);
            font-size: 14px;
            line-height: 1.6;
        }


        /* =========================================================
           CTA
        ========================================================= */

        .cta {
            padding: 90px 0;
        }

        .cta-box {
            padding: 65px 35px;

            text-align: center;

            border-radius: 32px;

            background:
                radial-gradient(
                    circle at 20% 10%,
                    rgba(255,255,255,.12),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #321064,
                    var(--purple-dark)
                );

            color: white;

            box-shadow:
                0 25px 70px rgba(91,33,182,.25);
        }

        .cta-box h2 {
            font-size: clamp(30px, 5vw, 48px);
            letter-spacing: -1.5px;
            margin-bottom: 15px;
        }

        .cta-box p {
            max-width: 600px;
            margin: 0 auto 28px;

            color: rgba(255,255,255,.78);
            line-height: 1.8;
        }


        /* =========================================================
           FOOTER
        ========================================================= */

        footer {
            padding: 35px 0;

            border-top: 1px solid var(--border);

            background: var(--bg-secondary);
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }

        .footer-name {
            font-weight: 800;
            font-size: 14px;
        }

        .footer-copy {
            color: var(--text-light);
            font-size: 12px;
        }


        /* =========================================================
           LANGUAGE CONTENT
        ========================================================= */

        .lang {
            display: none;
        }

        .lang.active {
            display: block;
        }


        /* =========================================================
           MOBILE
        ========================================================= */

        @media (max-width: 900px) {

            .nav-links {
                display: none;
            }

            .hero-grid,
            .about-grid,
            .clinic-grid {
                grid-template-columns: 1fr;
            }

            .hero {
                padding-top: 125px;
            }

            .doctor-wrap {
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

            .about-text h2 {
                font-size: 34px;
            }

            .doctor-badge {
                left: 10px;
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }

        @media (max-width: 560px) {

            .brand-text {
                display: none;
            }

            .language-select {
                font-size: 12px;
            }

            .hero h1 {
                font-size: 43px;
                letter-spacing: -2px;
            }

            .hero-description {
                font-size: 16px;
            }

            section {
                padding: 75px 0;
            }

            .quick-info {
                margin-top: 0;
            }

            .quick-grid {
                margin-top: 20px;
            }

            .doctor-card {
                width: 92%;
            }

            .hero-buttons {
                flex-direction: column;
            }

            .button {
                width: 100%;
            }
        }

    </style>
</head>


<body>

<!-- =============================================================
     NAVBAR
============================================================= -->

<header>

    <div class="container">

        <nav>

            <a href="#home" class="brand">

                <div class="brand-icon">
                    ♡
                </div>

                <div class="brand-text">
                    <span>Psychiatry & Mental Wellness</span>
                    <strong>Dr. Bebie Tagupa</strong>
                </div>

            </a>


            <div class="nav-links">

                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#services">Services</a>
                <a href="#clinic">Clinic</a>

            </div>


            <div class="nav-actions">

                <select
                    class="language-select"
                    id="languageSelect"
                    onchange="changeLanguage()"
                >
                    <option value="en">English</option>
                    <option value="fil">Filipino</option>
                    <option value="ceb">Visaya</option>
                </select>

                <button
                    class="theme-button"
                    onclick="toggleTheme()"
                    id="themeButton"
                    aria-label="Toggle dark mode"
                >
                    🌙
                </button>

            </div>

        </nav>

    </div>

</header>



<!-- =============================================================
     HERO
============================================================= -->

<main>

<section class="hero" id="home">

    <div class="container">

        <div class="hero-grid">


            <div>

                <div class="eyebrow">
                    ✦ Licensed Physician & Psychiatrist
                </div>


                <!-- ENGLISH -->

                <div class="lang active" data-lang="en">

                    <h1>
                        Your mind deserves
                        <span class="purple">care.</span>
                    </h1>

                    <p class="hero-description">
                        Compassionate, patient-centered psychiatric care
                        focused on helping you understand your mental
                        well-being, find support, and move toward a healthier
                        and more fulfilling life.
                    </p>

                    <div class="hero-buttons">

                        <a
                            href="#clinic"
                            class="button button-primary"
                        >
                            📅 View Clinic Schedule
                        </a>

                        <a
                            href="#about"
                            class="button button-secondary"
                        >
                            Meet Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <!-- FILIPINO -->

                <div class="lang" data-lang="fil">

                    <h1>
                        Ang iyong isip ay
                        <span class="purple">mahalaga.</span>
                    </h1>

                    <p class="hero-description">
                        Maalagang psychiatric care na nakatuon sa bawat
                        pasyente. Layunin naming tulungan kang maunawaan
                        ang iyong mental well-being at magkaroon ng mas
                        malusog at makabuluhang buhay.
                    </p>

                    <div class="hero-buttons">

                        <a
                            href="#clinic"
                            class="button button-primary"
                        >
                            📅 Tingnan ang Schedule
                        </a>

                        <a
                            href="#about"
                            class="button button-secondary"
                        >
                            Kilalanin si Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <!-- VISAYA -->

                <div class="lang" data-lang="ceb">

                    <h1>
                        Importante ang imong
                        <span class="purple">hunahuna.</span>
                    </h1>

                    <p class="hero-description">
                        Mainiton ug maloloy-on nga psychiatric care nga
                        nakasentro sa panginahanglan sa matag pasyente.
                        Ania kami aron motabang kanimo sa pag-atiman sa
                        imong mental well-being ug kinabuhi.
                    </p>

                    <div class="hero-buttons">

                        <a
                            href="#clinic"
                            class="button button-primary"
                        >
                            📅 Tan-awa ang Schedule
                        </a>

                        <a
                            href="#about"
                            class="button button-secondary"
                        >
                            Ilaila si Dr. Tagupa →
                        </a>

                    </div>

                </div>

            </div>



            <div class="doctor-wrap">

                <div class="doctor-glow"></div>

                <div class="doctor-card">

                    <!--
                    IMPORTANT:
                    Put the doctor's photo inside:
                    static/image0 (2).jpeg
                    -->

                    <img
                        src="{{ url_for('static', filename='image0 (2).jpeg') }}"
                        alt="Dr. Bebie Queen Lucelle R. Tagupa"
                        class="doctor-photo"
                    >

                    <div class="doctor-badge">

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



<!-- =============================================================
     QUICK INFO
============================================================= -->

<section class="quick-info">

    <div class="container">

        <div class="quick-grid">

            <div class="quick-card">

                <div class="quick-icon">🩺</div>

                <h3>
                    Licensed Physician
                </h3>

                <p>
                    Medical doctor committed to compassionate,
                    patient-centered care.
                </p>

            </div>


            <div class="quick-card">

                <div class="quick-icon">🧠</div>

                <h3>
                    Psychiatry
                </h3>

                <p>
                    Specialized training in psychiatric evaluation
                    and treatment.
                </p>

            </div>


            <div class="quick-card">

                <div class="quick-icon">💜</div>

                <h3>
                    Patient-Centered Care
                </h3>

                <p>
                    Your story, concerns, and well-being are at the
                    heart of every consultation.
                </p>

            </div>

        </div>

    </div>

</section>



<!-- =============================================================
     ABOUT
============================================================= -->

<section class="about" id="about">

    <div class="container">

        <div class="about-grid">


            <div class="about-card">

                <div class="quote">

                    “Mental health care begins
                    with <span>being heard.</span>”

                </div>

            </div>


            <div class="about-text">

                <div class="section-heading"
                     style="text-align:left;margin:0 0 25px 0;">

                    <div class="small-title">
                        About the Doctor
                    </div>

                </div>


                <div class="lang active" data-lang="en">

                    <h2>
                        Meet Dr. Tagupa
                    </h2>

                    <p>
                        Dr. Bebie Queen Lucelle R. Tagupa is a licensed
                        physician and psychiatrist dedicated to providing
                        compassionate and patient-centered mental health
                        care.
                    </p>

                    <p>
                        She earned her Bachelor’s degree in Medical
                        Technology from Velez College and is also a
                        licensed Medical Technologist.
                    </p>

                    <p>
                        She proceeded to study Medicine at Xavier University
                        – Ateneo de Cagayan.
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


                <div class="lang" data-lang="fil">

                    <h2>
                        Kilalanin si Dr. Tagupa
                    </h2>

                    <p>
                        Si Dr. Bebie Queen Lucelle R. Tagupa ay isang
                        licensed physician at psychiatrist na nakatuon sa
                        mahabagin at patient-centered na pangangalaga
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
                        Nakumpleto niya ang kanyang post-graduate
                        internship sa Davao Doctors Hospital at ang
                        residency training sa Psychiatry sa Southern
                        Philippines Medical Center – Institute of
                        Psychiatry and Behavioral Medicine.
                    </p>

                    <p>
                        Sa kanyang huling taon ng training, nagsilbi siya
                        bilang Chief Resident at ginawaran bilang
                        Most Outstanding Resident in Psychiatry.
                    </p>

                </div>


                <div class="lang" data-lang="ceb">

                    <h2>
                        Ilaila si Dr. Tagupa
                    </h2>

                    <p>
                        Si Dr. Bebie Queen Lucelle R. Tagupa usa ka
                        licensed physician ug psychiatrist nga
                        naghatag og maloloy-on ug patient-centered
                        nga mental health care.
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
                        Nakompleto niya ang post-graduate internship sa
                        Davao Doctors Hospital ug ang residency training
                        sa Psychiatry sa Southern Philippines Medical
                        Center – Institute of Psychiatry and Behavioral
                        Medicine.
                    </p>

                    <p>
                        Sa iyang katapusang tuig sa training, nagsilbi siya
                        isip Chief Resident ug nadawat ang award nga
                        Most Outstanding Resident in Psychiatry.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>



<!-- =============================================================
     CREDENTIALS
============================================================= -->

<section>

    <div class="container">

        <div class="section-heading">

            <div class="small-title">
                Experience & Training
            </div>

            <h2>
                A journey built on dedication.
            </h2>

            <p>
                A strong academic and clinical foundation dedicated
                to psychiatric care.
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
                    Professional medical laboratory background
                    before pursuing medicine.
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



<!-- =============================================================
     SERVICES
============================================================= -->

<section id="services" class="about">

    <div class="container">

        <div class="section-heading">

            <div class="small-title">
                Mental Health Care
            </div>

            <h2>
                Care that starts with you.
            </h2>

            <p>
                Dr. Tagupa provides psychiatric evaluation and
                treatment for a wide range of mental health concerns.
            </p>

        </div>


        <div class="services-grid">

            <div class="service-card">

                <div class="service-icon">
                    🧠
                </div>

                <h3>
                    Psychiatric Evaluation
                </h3>

                <p>
                    Comprehensive assessment to better understand
                    your mental health concerns and identify appropriate
                    treatment options.
                </p>

            </div>


            <div class="service-card">

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


            <div class="service-card">

                <div class="service-icon">
                    🌱
                </div>

                <h3>
                    Treatment & Follow-Up
                </h3>

                <p>
                    Patient-centered treatment and follow-up designed
                    around individual needs, goals, and progress.
                </p>

            </div>

        </div>

    </div>

</section>



<!-- =============================================================
     CARE JOURNEY
============================================================= -->

<section class="journey">

    <div class="container">

        <div class="section-heading">

            <div class="small-title">
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

            <div class="journey-step">

                <span>1</span>

                <h3>
                    Be Heard
                </h3>

                <p>
                    Share your concerns in a respectful and
                    supportive environment.
                </p>

            </div>


            <div class="journey-step">

                <span>2</span>

                <h3>
                    Understand
                </h3>

                <p>
                    Work toward understanding your mental health
                    and your individual needs.
                </p>

            </div>


            <div class="journey-step">

                <span>3</span>

                <h3>
                    Move Forward
                </h3>

                <p>
                    Develop an appropriate treatment plan and
                    continue working toward better well-being.
                </p>

            </div>

        </div>

    </div>

</section>



<!-- =============================================================
     CLINIC
============================================================= -->

<section id="clinic">

    <div class="container">

        <div class="section-heading">

            <div class="small-title">
                Clinic Information
            </div>

            <h2>
                Visit the clinic.
            </h2>

            <p>
                Find the clinic location and consultation schedule
                below.
            </p>

        </div>


        <div class="clinic-grid">


            <div class="clinic-card">

                <h3>
                    📍 Clinic
                </h3>


                <div class="clinic-row">

                    <div class="clinic-row-icon">
                        🏥
                    </div>

                    <div>

                        <strong>
                            Hospital
                        </strong>

                        <p>
                            Medina General Hospital
                        </p>

                    </div>

                </div>


                <div class="clinic-row">

                    <div class="clinic-row-icon">
                        🚪
                    </div>

                    <div>

                        <strong>
                            Location
                        </strong>

                        <p>
                            OPD Door 2
                        </p>

                    </div>

                </div>

            </div>



            <div class="clinic-card">

                <h3>
                    🕘 Consultation Schedule
                </h3>


                <div class="clinic-row">

                    <div class="clinic-row-icon">
                        📅
                    </div>

                    <div>

                        <strong>
                            Days
                        </strong>

                        <p>
                            Tuesday • Thursday • Saturday
                        </p>

                    </div>

                </div>


                <div class="clinic-row">

                    <div class="clinic-row-icon">
                        ⏰
                    </div>

                    <div>

                        <strong>
                            Time
                        </strong>

                        <p>
                            9:00 AM – 4:00 PM
                        </p>

                    </div>

                </div>

            </div>


        </div>

    </div>

</section>



<!-- =============================================================
     CTA
============================================================= -->

<section class="cta">

    <div class="container">

        <div class="cta-box">

            <h2>
                Your mental well-being matters.
            </h2>

            <p>
                Taking the first step toward better mental health
                can be difficult. You don't have to take that step
                alone.
            </p>

            <a
                href="#clinic"
                class="button"
                style="background:white;color:#5b21b6;"
            >
                View Clinic Schedule →
            </a>

        </div>

    </div>

</section>

</main>



<!-- =============================================================
     FOOTER
============================================================= -->

<footer>

    <div class="container">

        <div class="footer-content">

            <div>

                <div class="footer-name">
                    Dr. Bebie Queen Lucelle R. Tagupa
                </div>

                <div class="footer-copy">
                    Licensed Physician • Psychiatrist
                </div>

            </div>


            <div class="footer-copy">

                © 2026 Dr. Bebie Tagupa.
                All rights reserved.

            </div>

        </div>

    </div>

</footer>



<script>

    /* =========================================================
       LANGUAGE SWITCHER
    ========================================================= */

    function changeLanguage() {

        const selected =
            document.getElementById("languageSelect").value;

        document
            .querySelectorAll(".lang")
            .forEach(element => {

                element.classList.remove("active");

                if (element.dataset.lang === selected) {
                    element.classList.add("active");
                }

            });

        localStorage.setItem(
            "preferredLanguage",
            selected
        );
    }


    /* =========================================================
       DARK / LIGHT MODE
    ========================================================= */

    function toggleTheme() {

        document.body.classList.toggle("dark");

        const isDark =
            document.body.classList.contains("dark");

        localStorage.setItem(
            "darkMode",
            isDark ? "true" : "false"
        );

        updateThemeButton();
    }


    function updateThemeButton() {

        const button =
            document.getElementById("themeButton");

        const isDark =
            document.body.classList.contains("dark");

        button.textContent =
            isDark ? "☀️" : "🌙";
    }


    /* =========================================================
       LOAD SAVED SETTINGS
    ========================================================= */

    document.addEventListener(
        "DOMContentLoaded",
        function () {

            const savedLanguage =
                localStorage.getItem(
                    "preferredLanguage"
                );

            if (savedLanguage) {

                document.getElementById(
                    "languageSelect"
                ).value = savedLanguage;

                changeLanguage();
            }


            const savedDarkMode =
                localStorage.getItem("darkMode");

            if (savedDarkMode === "true") {

                document.body.classList.add("dark");

            }

            updateThemeButton();

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
    return {
        "status": "ok",
        "message": "Dr. Tagupa website is running."
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
"""

# Render / production entry point
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
