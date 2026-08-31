```python
from flask import Flask, render_template_string
import os

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Dr. Bebie Queen Lucelle R. Tagupa | Psychiatrist</title>

<meta
    name="description"
    content="Dr. Bebie Queen Lucelle R. Tagupa, licensed physician and psychiatrist. Compassionate, patient-centered psychiatric care."
>

<style>
:root{
    --purple:#7c3aed;
    --purple2:#5b21b6;
    --purple3:#a78bfa;
    --bg:#fbf9ff;
    --card:#ffffff;
    --text:#241532;
    --muted:#6f6380;
    --line:rgba(124,58,237,.14);
    --soft:#f0eaff;
    --shadow:0 18px 55px rgba(72,39,108,.12);
}

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html{
    scroll-behavior:smooth;
}

body{
    font-family:
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background:var(--bg);
    color:var(--text);
    line-height:1.6;
    transition:.25s;
}

body.dark{
    --bg:#100a17;
    --card:#1b1224;
    --text:#f8f2ff;
    --muted:#c1b3ce;
    --line:rgba(196,167,255,.18);
    --soft:#2a1b39;
    --shadow:0 18px 55px rgba(0,0,0,.36);
}

a{
    text-decoration:none;
    color:inherit;
}

button,
select{
    font:inherit;
}

.container{
    width:min(1120px,92%);
    margin:auto;
}

/* =========================
   HEADER
========================= */

header{
    position:fixed;
    z-index:999;
    top:0;
    left:0;
    width:100%;

    background:rgba(251,249,255,.82);
    backdrop-filter:blur(18px);

    border-bottom:1px solid var(--line);
}

body.dark header{
    background:rgba(16,10,23,.82);
}

nav{
    min-height:76px;

    display:flex;
    align-items:center;
    justify-content:space-between;

    gap:18px;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;

    font-weight:800;
}

.logo{
    width:44px;
    height:44px;

    border-radius:14px;

    color:white;

    display:grid;
    place-items:center;

    background:
        linear-gradient(
            135deg,
            var(--purple),
            var(--purple2)
        );

    box-shadow:
        0 10px 25px rgba(124,58,237,.25);
}

.brand small{
    display:block;

    color:var(--purple);

    text-transform:uppercase;
    letter-spacing:1.4px;

    font-size:10px;
}

.brand strong{
    display:block;
    font-size:15px;
}

.navlinks{
    display:flex;
    gap:24px;
}

.navlinks a{
    font-size:14px;
    font-weight:700;
    color:var(--muted);

    transition:.2s;
}

.navlinks a:hover{
    color:var(--purple);
}

.actions{
    display:flex;
    gap:8px;
    align-items:center;
}

select,
.theme{
    border:1px solid var(--line);
    background:var(--card);
    color:var(--text);

    border-radius:12px;
    height:40px;
}

select{
    padding:0 10px;
}

.theme{
    width:40px;
    cursor:pointer;
}

/* =========================
   HERO
========================= */

.hero{
    padding:145px 0 85px;
}

.hero-grid{
    display:grid;
    grid-template-columns:1.05fr .95fr;
    align-items:center;
    gap:64px;
}

.pill{
    display:inline-flex;

    padding:8px 13px;

    border-radius:999px;

    background:var(--soft);
    color:var(--purple2);

    font-size:11px;
    font-weight:900;

    text-transform:uppercase;
    letter-spacing:1.2px;

    margin-bottom:19px;
}

body.dark .pill{
    color:#dfd0ff;
}

h1{
    font-size:clamp(42px,6vw,72px);
    line-height:1.03;

    letter-spacing:-3px;

    margin-bottom:22px;
}

.grad{
    color:var(--purple);
}

.lead{
    font-size:18px;
    color:var(--muted);

    max-width:620px;

    margin-bottom:30px;
}

.buttons{
    display:flex;
    gap:12px;
    flex-wrap:wrap;
}

.btn{
    display:inline-flex;

    align-items:center;
    justify-content:center;

    min-height:50px;

    padding:0 20px;

    border-radius:14px;

    font-weight:800;
    font-size:14px;

    transition:.2s;
}

.primary{
    color:white;

    background:
        linear-gradient(
            135deg,
            var(--purple),
            var(--purple2)
        );

    box-shadow:
        0 14px 30px rgba(124,58,237,.22);
}

.primary:hover{
    transform:translateY(-3px);
}

.secondary{
    background:var(--card);
    border:1px solid var(--line);
}

.secondary:hover{
    transform:translateY(-3px);
    border-color:var(--purple3);
}

/* =========================
   DOCTOR PHOTO
========================= */

.photo-wrap{
    position:relative;

    display:flex;
    justify-content:center;
}

.photo-glow{
    position:absolute;

    width:390px;
    height:390px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(124,58,237,.28),
            transparent 67%
        );
}

.photo-card{
    position:relative;

    width:min(420px,100%);

    padding:11px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #eee7ff
        );

    border-radius:32px;

    box-shadow:var(--shadow);

    transform:rotate(1deg);
}

body.dark .photo-card{
    background:
        linear-gradient(
            145deg,
            #39264d,
            #1d1327
        );
}

.photo{
    width:100%;

    aspect-ratio:4/5;

    object-fit:cover;
    object-position:center;

    display:block;

    border-radius:23px;

    background:var(--soft);
}

.badge{
    position:absolute;

    left:-24px;
    bottom:26px;

    padding:16px 18px;

    border:1px solid var(--line);

    background:var(--card);

    border-radius:17px;

    box-shadow:var(--shadow);
}

.badge b{
    display:block;
    font-size:13px;
}

.badge span{
    font-size:11px;
    color:var(--muted);
}

/* =========================
   QUICK CARDS
========================= */

.quick{
    margin-top:-22px;

    position:relative;
    z-index:2;
}

.quickgrid{
    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:15px;
}

.quickcard{
    padding:24px;

    border:1px solid var(--line);

    background:var(--card);

    border-radius:20px;

    box-shadow:var(--shadow);
}

.quickcard .icon{
    font-size:24px;
    margin-bottom:10px;
}

.quickcard h3{
    font-size:16px;
    margin-bottom:5px;
}

.quickcard p{
    font-size:13px;
    color:var(--muted);
}

/* =========================
   SECTIONS
========================= */

section{
    padding:100px 0;
}

.alt{
    background:var(--soft);
}

.heading{
    text-align:center;

    max-width:720px;

    margin:
        0 auto 48px;
}

.kicker{
    color:var(--purple);

    font-size:11px;

    letter-spacing:2px;

    text-transform:uppercase;

    font-weight:900;

    margin-bottom:10px;
}

.heading h2{
    font-size:
        clamp(
            31px,
            5vw,
            48px
        );

    line-height:1.1;

    letter-spacing:-1.8px;

    margin-bottom:13px;
}

.heading p{
    color:var(--muted);
}

/* =========================
   ABOUT
========================= */

.aboutgrid{
    display:grid;

    grid-template-columns:
        .78fr 1.22fr;

    gap:58px;

    align-items:center;
}

.aboutquote{
    padding:34px;

    background:var(--card);

    border:1px solid var(--line);

    border-radius:27px;

    box-shadow:var(--shadow);

    font-size:28px;

    font-weight:850;

    line-height:1.3;
}

.aboutquote span{
    color:var(--purple);
}

.abouttext h2{
    font-size:41px;

    letter-spacing:-1.5px;

    margin-bottom:17px;
}

.abouttext p{
    color:var(--muted);
    margin-bottom:14px;
}

/* =========================
   CREDENTIALS
========================= */

.credgrid{
    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:16px;
}

.cred{
    padding:22px;

    background:var(--card);

    border:1px solid var(--line);

    border-radius:19px;
}

.cred b{
    font-size:11px;

    color:var(--purple);

    letter-spacing:1px;
}

.cred h3{
    font-size:16px;

    margin:
        7px 0 3px;
}

.cred p{
    font-size:13px;
    color:var(--muted);
}

/* =========================
   SERVICES
========================= */

.grid3{
    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:20px;
}

.card{
    padding:29px;

    border:1px solid var(--line);

    background:var(--card);

    border-radius:23px;

    box-shadow:var(--shadow);

    position:relative;

    overflow:hidden;
}

.card:before{
    content:"";

    position:absolute;

    left:0;
    right:0;
    top:0;

    height:4px;

    background:
        linear-gradient(
            90deg,
            var(--purple),
            var(--purple3)
        );
}

.cardicon{
    width:53px;
    height:53px;

    display:grid;
    place-items:center;

    background:var(--soft);

    border-radius:15px;

    font-size:24px;

    margin-bottom:18px;
}

.card h3{
    margin-bottom:8px;
    font-size:18px;
}

.card p{
    color:var(--muted);
    font-size:14px;
}

/* =========================
   CARE JOURNEY
========================= */

.band{
    background:
        linear-gradient(
            135deg,
            var(--purple2),
            var(--purple)
        );

    color:white;
}

.band .heading p{
    color:rgba(255,255,255,.78);
}

.steps{
    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:20px;
}

.step{
    padding:28px;

    border:
        1px solid
        rgba(255,255,255,.16);

    background:
        rgba(255,255,255,.09);

    border-radius:22px;
}

.stepnum{
    width:42px;
    height:42px;

    border-radius:50%;

    display:grid;
    place-items:center;

    background:
        rgba(255,255,255,.14);

    font-weight:900;

    margin-bottom:15px;
}

.step p{
    color:
        rgba(255,255,255,.78);

    font-size:14px;
}

/* =========================
   CLINIC
========================= */

.clinicgrid{
    display:grid;

    grid-template-columns:
        1fr 1fr;

    gap:20px;
}

.clinic{
    padding:31px;

    background:var(--card);

    border:1px solid var(--line);

    border-radius:23px;

    box-shadow:var(--shadow);
}

.clinic h3{
    font-size:21px;
    margin-bottom:15px;
}

.row{
    display:flex;

    gap:13px;

    align-items:flex-start;

    padding:15px 0;

    border-bottom:
        1px solid
        var(--line);
}

.row:last-child{
    border-bottom:0;
}

.rowicon{
    width:41px;
    height:41px;

    flex:none;

    border-radius:12px;

    display:grid;
    place-items:center;

    background:var(--soft);
}

.row b{
    display:block;
    font-size:14px;
}

.row span{
    color:var(--muted);
    font-size:14px;
}

/* =========================
   CTA
========================= */

.cta{
    padding:80px 0;
}

.ctabox{
    text-align:center;

    padding:62px 30px;

    border-radius:31px;

    color:white;

    background:
        linear-gradient(
            135deg,
            #32105f,
            var(--purple2)
        );

    box-shadow:
        0 24px 65px
        rgba(91,33,182,.25);
}

.ctabox h2{
    font-size:
        clamp(
            30px,
            5vw,
            48px
        );

    letter-spacing:-1.5px;

    margin-bottom:11px;
}

.ctabox p{
    max-width:610px;

    margin:
        0 auto 25px;

    color:
        rgba(255,255,255,.78);
}

/* =========================
   FOOTER
========================= */

footer{
    padding:33px 0;

    background:var(--soft);

    border-top:
        1px solid
        var(--line);
}

.footerrow{
    display:flex;

    justify-content:space-between;

    gap:20px;

    align-items:center;
}

.footerrow strong{
    font-size:14px;
}

.footerrow span{
    font-size:12px;
    color:var(--muted);
}

/* =========================
   LANGUAGE
========================= */

.lang{
    display:none;
}

.lang.active{
    display:block;
}

/* =========================
   RESPONSIVE
========================= */

@media(max-width:900px){

    .navlinks{
        display:none;
    }

    .hero-grid,
    .aboutgrid,
    .clinicgrid{
        grid-template-columns:1fr;
    }

    .photo-wrap{
        order:-1;
    }

    .quickgrid,
    .grid3,
    .steps{
        grid-template-columns:1fr;
    }

    .credgrid{
        grid-template-columns:1fr;
    }

    .quick{
        margin-top:0;
    }

    .abouttext h2{
        font-size:34px;
    }

    .footerrow{
        flex-direction:column;
        text-align:center;
    }
}

@media(max-width:560px){

    .brand small,
    .brand strong{
        display:none;
    }

    .hero{
        padding-top:120px;
    }

    h1{
        font-size:43px;
        letter-spacing:-2px;
    }

    .lead{
        font-size:16px;
    }

    .buttons{
        flex-direction:column;
    }

    .btn{
        width:100%;
    }

    .badge{
        left:9px;
    }

    section{
        padding:74px 0;
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


            <div class="navlinks">

                <a href="#home">
                    Home
                </a>

                <a href="#about">
                    About
                </a>

                <a href="#services">
                    Services
                </a>

                <a href="#clinic">
                    Clinic
                </a>

            </div>


            <div class="actions">

                <select
                    id="lang"
                    onchange="setLanguage(this.value)"
                    aria-label="Language"
                >

                    <option value="en">
                        English
                    </option>

                    <option value="fil">
                        Filipino
                    </option>

                    <option value="ceb">
                        Visaya
                    </option>

                </select>


                <button
                    class="theme"
                    id="theme"
                    onclick="toggleTheme()"
                    aria-label="Toggle dark mode"
                >
                    🌙
                </button>

            </div>

        </nav>

    </div>

</header>


<main>

<!-- =========================
     HERO
========================= -->

<section
    class="hero"
    id="home"
>

    <div class="container">

        <div class="hero-grid">


            <div>

                <div class="pill">
                    ✦ Licensed Physician & Psychiatrist
                </div>


                <!-- ENGLISH -->

                <div
                    class="lang active"
                    data-lang="en"
                >

                    <h1>
                        Your mind deserves
                        <span class="grad">
                            care.
                        </span>
                    </h1>

                    <p class="lead">
                        Compassionate, patient-centered psychiatric
                        care focused on helping you understand your
                        mental well-being, find support, and move
                        toward a healthier and more fulfilling life.
                    </p>

                    <div class="buttons">

                        <a
                            class="btn primary"
                            href="#clinic"
                        >
                            📅 View Clinic Schedule
                        </a>

                        <a
                            class="btn secondary"
                            href="#about"
                        >
                            Meet Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <!-- FILIPINO -->

                <div
                    class="lang"
                    data-lang="fil"
                >

                    <h1>
                        Ang iyong isip ay
                        <span class="grad">
                            mahalaga.
                        </span>
                    </h1>

                    <p class="lead">
                        Maalagang psychiatric care na nakatuon sa bawat
                        pasyente. Layunin naming tulungan kang maunawaan
                        ang iyong mental well-being at magkaroon ng mas
                        malusog at makabuluhang buhay.
                    </p>

                    <div class="buttons">

                        <a
                            class="btn primary"
                            href="#clinic"
                        >
                            📅 Tingnan ang Schedule
                        </a>

                        <a
                            class="btn secondary"
                            href="#about"
                        >
                            Kilalanin si Dr. Tagupa →
                        </a>

                    </div>

                </div>


                <!-- VISAYA -->

                <div
                    class="lang"
                    data-lang="ceb"
                >

                    <h1>
                        Importante ang imong
                        <span class="grad">
                            hunahuna.
                        </span>
                    </h1>

                    <p class="lead">
                        Mainiton ug maloloy-on nga psychiatric care
                        nga nakasentro sa panginahanglan sa matag
                        pasyente. Ania kami aron motabang kanimo sa
                        pag-atiman sa imong mental well-being ug kinabuhi.
                    </p>

                    <div class="buttons">

                        <a
                            class="btn primary"
                            href="#clinic"
                        >
                            📅 Tan-awa ang Schedule
                        </a>

                        <a
                            class="btn secondary"
                            href="#about"
                        >
                            Ilaila si Dr. Tagupa →
                        </a>

                    </div>

                </div>

            </div>


            <div class="photo-wrap">

                <div class="photo-glow"></div>

                <div class="photo-card">

                    <img
                        class="photo"
                        src="/static/image0%20%282%29.jpeg"
                        alt="Dr. Bebie Queen Lucelle R. Tagupa"
                    >

                    <div class="badge">

                        <b>
                            Dr. Bebie Queen Lucelle R. Tagupa
                        </b>

                        <span>
                            Licensed Physician • Psychiatrist
                        </span>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- =========================
     QUICK CARDS
========================= -->

<section class="quick">

    <div class="container">

        <div class="quickgrid">

            <div class="quickcard">

                <div class="icon">
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


            <div class="quickcard">

                <div class="icon">
                    🧠
                </div>

                <h3>
                    Psychiatry
                </h3>

                <p>
                    Specialized training in psychiatric
                    evaluation and treatment.
                </p>

            </div>


            <div class="quickcard">

                <div class="icon">
                    💜
                </div>

                <h3>
                    Patient-Centered Care
                </h3>

                <p>
                    Your story and well-being are at the heart
                    of every consultation.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- =========================
     ABOUT
========================= -->

<section
    class="alt"
    id="about"
>

    <div class="container">

        <div class="aboutgrid">

            <div class="aboutquote">

                “Mental health care begins with
                <span>
                    being heard.
                </span>”

            </div>


            <div class="abouttext">

                <div class="kicker">
                    About the Doctor
                </div>


                <!-- ENGLISH -->

                <div
                    class="lang active"
                    data-lang="en"
                >

                    <h2>
                        Meet Dr. Tagupa
                    </h2>

                    <p>
                        Dr. Bebie Queen Lucelle R. Tagupa is a
                        licensed physician and psychiatrist
                        dedicated to providing compassionate and
                        patient-centered mental health care.
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
                        She completed her post-graduate internship
                        at Davao Doctors Hospital and finished her
                        residency training in Psychiatry at the
                        Southern Philippines Medical Center –
                        Institute of Psychiatry and Behavioral Medicine.
                    </p>

                    <p>
                        During her final year of training, she served
                        as Chief Resident and was awarded Most
                        Outstanding Resident in Psychiatry during
                        her graduation.
                    </p>

                </div>


                <!-- FILIPINO -->

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
                        Sa kanyang huling taon ng training, nagsilbi
                        siya bilang Chief Resident at ginawaran bilang
                        Most Outstanding Resident in Psychiatry.
                    </p>

                </div>


                <!-- VISAYA -->

                <div
                    class="lang"
                    data-lang="ceb"
                >

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


<!-- =========================
     EDUCATION
========================= -->

<section>

    <div class="container">

        <div class="heading">

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


        <div class="credgrid">

            <div class="cred">

                <b>01</b>

                <h3>
                    Bachelor of Medical Technology
                </h3>

                <p>
                    Velez College
                </p>

            </div>


            <div class="cred">

                <b>02</b>

                <h3>
                    Licensed Medical Technologist
                </h3>

                <p>
                    Professional medical laboratory background.
                </p>

            </div>


            <div class="cred">

                <b>03</b>

                <h3>
                    Doctor of Medicine
                </h3>

                <p>
                    Xavier University – Ateneo de Cagayan
                </p>

            </div>


            <div class="cred">

                <b>04</b>

                <h3>
                    Post-Graduate Internship
                </h3>

                <p>
                    Davao Doctors Hospital
                </p>

            </div>


            <div class="cred">

                <b>05</b>

                <h3>
                    Psychiatry Residency
                </h3>

                <p>
                    Southern Philippines Medical Center –
                    Institute of Psychiatry and Behavioral Medicine
                </p>

            </div>


            <div class="cred">

                <b>06</b>

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


<!-- =========================
     SERVICES
========================= -->

<section
    class="alt"
    id="services"
>

    <div class="container">

        <div class="heading">

            <div class="kicker">
                Mental Health Care
            </div>

            <h2>
                Care that starts with you.
            </h2>

            <p>
                Dr. Tagupa provides psychiatric evaluation and
                treatment for a wide range of mental health conditions.
            </p>

        </div>


        <div class="grid3">

            <div class="card">

                <div class="cardicon">
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


            <div class="card">

                <div class="cardicon">
                    💬
                </div>

                <h3>
                    Mental Health Consultation
                </h3>

                <p>
                    A respectful space to discuss concerns, emotions,
                    thoughts, behavior, and overall mental well-being.
                </p>

            </div>


            <div class="card">

                <div class="cardicon">
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


<!-- =========================
     CARE JOURNEY
========================= -->

<section class="band">

    <div class="container">

        <div class="heading">

            <div
                class="kicker"
                style="color:#e4d8ff"
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


        <div class="steps">

            <div class="step">

                <div class="stepnum">
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

                <div class="stepnum">
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

                <div class="stepnum">
                    3
                </div>

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


<!-- =========================
     CLINIC
========================= -->

<section id="clinic">

    <div class="container">

        <div class="heading">

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


        <div class="clinicgrid">


            <div class="clinic">

                <h3>
                    📍 Clinic
                </h3>


                <div class="row">

                    <div class="rowicon">
                        🏥
                    </div>

                    <div>

                        <b>
                            Hospital
                        </b>

                        <span>
                            Medina General Hospital
                        </span>

                    </div>

                </div>


                <div class="row">

                    <div class="rowicon">
                        🚪
                    </div>

                    <div>

                        <b>
                            Location
                        </b>

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


                <div class="row">

                    <div class="rowicon">
                        📅
                    </div>

                    <div>

                        <b>
                            Days
                        </b>

                        <span>
                            Tuesday • Thursday • Saturday
                        </span>

                    </div>

                </div>


                <div class="row">

                    <div class="rowicon">
                        ⏰
                    </div>

                    <div>

                        <b>
                            Time
                        </b>

                        <span>
                            9:00 AM – 4:00 PM
                        </span>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- =========================
     CTA
========================= -->

<section class="cta">

    <div class="container">

        <div class="ctabox">

            <h2>
                Your mental well-being matters.
            </h2>

            <p>
                Taking the first step toward better mental health
                can be difficult. You don't have to take that step alone.
            </p>

            <a
                class="btn"
                style="background:#fff;color:#5b21b6"
                href="#clinic"
            >
                View Clinic Schedule →
            </a>

        </div>

    </div>

</section>

</main>


<!-- =========================
     FOOTER
========================= -->

<footer>

    <div class="container">

        <div class="footerrow">

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

function setLanguage(value){

    document
        .querySelectorAll(".lang")
        .forEach(function(el){

            el.classList.toggle(
                "active",
                el.dataset.lang === value
            );

        });

    localStorage.setItem(
        "language",
        value
    );
}


function toggleTheme(){

    document.body.classList.toggle("dark");

    var dark =
        document.body.classList.contains("dark");

    localStorage.setItem(
        "dark",
        dark ? "1" : "0"
    );

    document.getElementById(
        "theme"
    ).textContent =
        dark ? "☀️" : "🌙";
}


(function(){

    var language =
        localStorage.getItem("language") || "en";

    var dark =
        localStorage.getItem("dark") === "1";


    document.getElementById(
        "lang"
    ).value = language;


    setLanguage(language);


    if(dark){

        document.body.classList.add("dark");

    }


    document.getElementById(
        "theme"
    ).textContent =
        dark ? "☀️" : "🌙";

})();

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


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
