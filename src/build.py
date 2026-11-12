"""Builds the static site into public/ from src/.

Run: python3 src/build.py
Edit colors and fonts in src/site.css. Edit content in src/partials/.
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "public"
PHONE = "417-496-3821"
TEL = "tel:+14174963821"
NAME = "Home Accessibility Solutions"

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("who-we-help.html", "Who We Help"),
    ("our-work.html", "Our Work"),
    ("how-it-works.html", "How It Works"),
    ("paying-for-it.html", "Paying for It"),
    ("care-teams.html", "For Care Teams"),
    ("about.html", "About David"),
]

PAGES = {
    "index.html": dict(
        title=f"{NAME} · David Edge · Springfield, MO",
        desc="Mom or Dad coming home? Steps getting harder? David Edge builds steps, ramps, grab bars, wider doorways and accessible cabinets that fit your home. Springfield, Missouri. Call 417-496-3821.",
        parts=["top", "statement", "paths", "services", "home-more", "how", "call"]),
    "services.html": dict(
        title=f"Services · {NAME}",
        desc="Steps, ramps, grab bars, wider doorways, accessible cabinets and kitchen retrofits, built by David Edge in Springfield, MO.",
        parts=["head-services", "services", "retrofits", "call"]),
    "who-we-help.html": dict(
        title=f"Who We Help · {NAME}",
        desc="Help for families getting a parent's home ready, homeowners who want to stay put, and people healing from surgery or an injury.",
        parts=["head-who", "family", "healing", "yourhome", "call"]),
    "our-work.html": dict(
        title=f"Our Work · {NAME}",
        desc="Real photos of steps, grab bars and custom cabinets built by David Edge.",
        parts=["head-work", "work", "call"]),
    "how-it-works.html": dict(
        title=f"How It Works · {NAME}",
        desc="Call David, he visits your home, you get a written quote, then he builds and checks back. Plus answers to common questions.",
        parts=["head-how", "how", "faq", "call"]),
    "paying-for-it.html": dict(
        title=f"Paying for It · {NAME}",
        desc="David Edge does VA and insurance work and helps families sort out what may help pay for home changes.",
        parts=["paying", "call"]),
    "care-teams.html": dict(
        title=f"For Care Teams · {NAME}",
        desc="OTs, PTs, discharge planners and case managers: refer a patient to David Edge for home changes built to your notes.",
        parts=["head-care", "partners", "call"]),
    "about.html": dict(
        title=f"About David · {NAME}",
        desc="David Edge is a Springfield, Missouri carpenter who builds home changes that help people stay in the homes they love.",
        parts=["about", "call"]),
}

# Sections that keep their own background.

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'

SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"Home Accessibility Solutions","slogan":"Helping you make your home work for you","founder":{"@type":"Person","name":"David Edge"},"telephone":"+1-417-496-3821","areaServed":"Springfield, Missouri","address":{"@type":"PostalAddress","addressLocality":"Springfield","addressRegion":"MO","addressCountry":"US"},"makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":"Entry steps and access ramps"}},{"@type":"Offer","itemOffered":{"@type":"Service","name":"Grab bars"}},{"@type":"Offer","itemOffered":{"@type":"Service","name":"Doorway widening"}},{"@type":"Offer","itemOffered":{"@type":"Service","name":"Accessible custom cabinets"}}]}
</script>"""


def nav_html(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(items)


def header(current):
    links = nav_html(current)
    return f"""<a class="skip" href="#main">Skip to main content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html">{NAME}<small>David Edge, owner · Springfield, MO</small></a>
    <a class="call" href="{TEL}" aria-label="Call David at {PHONE}">{PHONE_SVG}<span><span class="long">Call David </span>{PHONE}</span></a>
  </div>
</header>
<nav class="tabs" aria-label="Main">
  <div class="wrap">
    <ul class="tab-list">
{links}
    </ul>
    <details class="menu">
      <summary>Menu</summary>
      <ul>
{links}
      </ul>
    </details>
  </div>
</nav>"""


FOOTER = f"""<footer>
  <div class="wrap foot-grid">
    <div>
      <p class="wordmark">Home Accessibility<br>Solutions</p>
      <p>David Edge, owner · Springfield, Missouri<br><a href="{TEL}">{PHONE}</a></p>
    </div>
    <ul class="foot-links">{"".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)}</ul>
  </div>
</footer>"""


def load(name):
    return (SRC / "partials" / f"{name}.html").read_text()


def stripe(html):
    """Alternate backgrounds on plain sections, section by section."""
    fixed = ("hero", "statement", "paths", "page-head", "partners", "close")
    chunks = re.split(r'(?=  <section)', html)
    out, alt = [], False
    for ch in chunks:
        m = re.match(r'\s*<section(?: class="([^"]*)")?', ch)
        if not m:
            out.append(ch)
            continue
        classes = (m.group(1) or "").split()
        if any(c in fixed for c in classes):
            out.append(ch)
            alt = any(c in ("paths", "page-head") for c in classes)
            continue
        classes = [c for c in classes if c != "alt"]
        if alt:
            classes.insert(0, "alt")
        attr = f' class="{" ".join(classes)}"' if classes else ""
        ch = re.sub(r'<section(?: class="[^"]*")?', f"<section{attr}", ch, count=1)
        out.append(ch)
        alt = not alt
    return "".join(out)


def trim_head(html, sid):
    """Drop a section's own h2 and intro when the page already has a page head."""
    return re.sub(r'(<section[^>]*id="%s"[^>]*>\s*<div class="wrap">)\s*<h2[^>]*>.*?</h2>\s*<p class="intro">.*?</p>' % sid,
                  r"\1", html, count=1, flags=re.S).replace(f'id="{sid}" aria-labelledby="h-{sid}"', f'id="{sid}"')


def build():
    if OUT.exists():
        for p in OUT.glob("*.html"):
            p.unlink()
    (OUT / "css").mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC / "site.css", OUT / "css" / "site.css")
    for fname, page in PAGES.items():
        body = "".join(load(n) for n in page["parts"])
        if fname != "index.html":
            for sid in ("services", "how"):
                body = trim_head(body, sid)
        body = stripe(body)
        schema = SCHEMA if fname == "index.html" else ""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Inter+Tight:wght@500;600&family=Instrument+Serif&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
{schema}
</head>
<body>
{header(fname)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""
        (OUT / fname).write_text(html)
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    build()
