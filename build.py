#!/usr/bin/env python3
"""Generate interior pages and the knowledge base for amarach.net.

Usage: python3 build.py
Reads content/knowledge/*.md, writes knowledge/*.html and the section pages.
index.html (Home) is authored directly and not touched here.
"""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
PHONE = "815-636-8311"
TEL = "tel:+18156368311"

NAV = [
    ("/", "Home"),
    ("/services/", "Services"),
    ("/dave-perfect/", "Dave Perfect"),
    ("/knowledge/", "Knowledge Base"),
    ("/about/", "About"),
    ("/contact/", "Contact"),
]


def shell(title, description, body, current, depth=1):
    prefix = "../" * depth
    current_attr = ' aria-current="page"'
    nav_items = "\n        ".join(
        f'<li><a href="{href}"{current_attr if href == current else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" href="/brand/icon-favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/site.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Amárach Net Solutions home">
      <img src="/brand/logo-horizontal.svg" alt="Amárach Net Solutions" width="760" height="200">
    </a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        {nav_items}
      </ul>
    </nav>
    <a class="header-phone" href="{TEL}">{PHONE}</a>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div>
      <a class="logo" href="/" aria-label="Amárach Net Solutions home">
        <img src="/brand/logo-horizontal-reversed.svg" alt="Amárach Net Solutions" width="760" height="200">
      </a>
      <p class="tagline">Serving the Rock River Valley since 1997.</p>
    </div>
    <div>
      <ul>
        <li><a href="{TEL}">{PHONE}</a></li>
        <li><a href="mailto:davidjp@amarach.net">davidjp@amarach.net</a></li>
        <li>On-site: the Rockford region and northern Illinois</li>
        <li>Remote: anywhere</li>
      </ul>
    </div>
    <div>
      <ul>
        <li><a href="/services/">Services</a></li>
        <li><a href="/dave-perfect/">Dave Perfect</a></li>
        <li><a href="/knowledge/">Knowledge Base</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-meta">
    <p>Founded by David JP Lickteig, Microsoft Certified Professional &middot; Rockford, Illinois</p>
  </div>
</footer>

</body>
</html>
"""


def parse_article(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    fm = dict(
        line.split(":", 1) for line in m.group(1).splitlines() if ":" in line
    )
    fm = {k.strip(): v.strip() for k, v in fm.items()}
    fm["slug"] = path.stem
    fm["html"] = markdown.markdown(m.group(2), extensions=["smarty"])
    return fm


def read_time(html):
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    return max(1, round(words / 220))


def build_knowledge():
    articles = [parse_article(p) for p in sorted((ROOT / "content/knowledge").glob("*.md"))]
    articles = [a for a in articles if a.get("public", "true") == "true"]
    articles.sort(key=lambda a: a["date"], reverse=True)

    categories = ["Getting Started", "Troubleshooting", "Security & Backups",
                  "Hardware", "Email & Internet", "FAQ"]
    used = [c for c in categories if any(a["category"] == c for a in articles)]

    for a in articles:
        minutes = read_time(a["html"])
        body = f"""
  <article class="section" style="padding-top: calc(var(--section) * 0.7);">
    <div class="wrap">
      <div class="prose">
        <p class="meta article-meta">{a['category']} &middot; Updated {a['date']} &middot; {minutes} min read</p>
        <h1>{a['title']}</h1>
        {a['html']}
        <p class="article-foot"><a href="/knowledge/">&larr; All articles</a></p>
      </div>
    </div>
  </article>
"""
        out = ROOT / "knowledge" / a["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(shell(f"{a['title']} | Amárach Net Solutions",
                             a["summary"], body, "/knowledge/", depth=2))

    cards = "\n".join(f"""
        <li class="kb-card">
          <p class="meta">{a['category']} &middot; {a['date']}</p>
          <h2><a href="/knowledge/{a['slug']}/">{a['title']}</a></h2>
          <p>{a['summary']}</p>
        </li>""" for a in articles)
    filters = "\n        ".join(f'<a href="#{c.lower().replace(" & ", "-").replace(" ", "-")}">{c}</a>' for c in used)
    body = f"""
  <div class="page-hero">
    <div class="wrap">
      <p class="meta kicker">Knowledge base</p>
      <h1>Fixes, explanations, and straight answers</h1>
      <p class="lede">The questions we get most, answered the way we'd answer them on the phone. Free to read, no login.</p>
    </div>
  </div>
  <section class="section" style="padding-top: 0;">
    <div class="wrap">
      <ul class="kb-list">
{cards}
      </ul>
    </div>
  </section>
"""
    (ROOT / "knowledge" / "index.html").write_text(
        shell("Knowledge Base | Amárach Net Solutions",
              "Fixes, explanations, and answers to the questions Rockford-area businesses ask us most. Free to read, no login.",
              body, "/knowledge/"))
    return articles


SERVICES = [
    ("Network administration",
     "The recurring work that keeps the interesting failures from happening.",
     ["Windows Server and Active Directory", "File, print, and permissions",
      "Remote access done safely", "Patching and updates, verified",
      "Backup checks that actually restore", "Monitoring and maintenance schedules"]),
    ("Equipment acquisition and provisioning",
     "Specified, sourced, and delivered working. You don't research part numbers; you tell us what the job is.",
     ["Hardware spec'd to the actual work", "Sourcing at fair cost",
      "Imaging and clean setup", "Migration of files, settings, and profiles",
      "Responsible disposal of the old unit",
      "Every machine delivered Dave Perfect"]),
    ("Vertical software integration",
     "Practice management, imaging, ERP, and other field-specific systems: installed, updated, and made to work with the rest of your network.",
     ["Installation and version upgrades", "Vendor coordination. We sit on hold so you don't have to",
      "Integration with your network, printers, and backups",
      "Dental, medical, professional, and industrial systems"]),
    ("Diagnosis and troubleshooting",
     "Figuring out what is actually wrong. Twenty-nine years of pattern recognition.",
     ["Intermittent faults and mystery noises", "Slow performance, found and fixed",
      "Printing, email, and connectivity", "Second opinions before you spend money"]),
    ("Support, on-site and remote",
     "Routine help for staff, one-off emergencies, and standing arrangements. Think of the remote side as telemedicine for your network: most problems are diagnosed and fixed without anyone waiting for a visit.",
     ["Remote sessions for most issues, usually within the hour",
      "On-site visits when it needs hands, across the Rockford region and northern Illinois",
      "Fully remote care of workstations and servers for clients beyond driving distance",
      "Standing maintenance arrangements for offices that would rather not think about it"]),
]


def build_services():
    blocks = "\n".join(f"""
      <div class="service-block">
        <h2>{name}</h2>
        <p>{lede}</p>
        <div class="prose"><ul>
          {''.join(f'<li>{item}</li>' for item in items)}
        </ul></div>
      </div>""" for name, lede, items in SERVICES)
    body = f"""
  <div class="page-hero">
    <div class="wrap">
      <p class="meta kicker">Services</p>
      <h1>One firm, accountable, that has seen your problem before</h1>
      <p class="lede">Amárach handles the whole stack a small business runs on: the network, the machines, and the software that's specific to your field. One number to call, and no vendor pointing at another vendor.</p>
    </div>
  </div>
  <section class="section" style="padding-top: calc(var(--section) * 0.4);">
    <div class="wrap">
{blocks}
    </div>
  </section>
  <section class="section section--navy closing">
    <div class="wrap">
      <p>Not sure which of these your problem is? That's fine. That's our job.</p>
      <a class="phone-big" href="{TEL}">Call {PHONE}</a>
    </div>
  </section>
"""
    out = ROOT / "services" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell("Services | Amárach Net Solutions",
                         "Network administration, equipment provisioning, vertical software, troubleshooting, and ongoing support for Rockford-area businesses.",
                         body, "/services/"))


def build_dave_perfect():
    steps = [
        "Inventory and baseline: what's installed, what's running, what's actually using the resources",
        "Remove bundled trials, redundant utilities, and unnecessary startup items",
        "Correct system and registry settings for how the machine will really be used",
        "Current drivers, firmware, and updates, verified rather than assumed",
        "Security and backup confirmed working",
        "Files, settings, and profiles migrated if it's a replacement",
        "Line-of-business and vertical software installed and tested",
        "Final pass: thermals, noise, boot time, and a real-world speed check",
    ]
    steps_html = "\n        ".join(f"<li>{s}</li>" for s in steps)
    body = f"""
  <div class="page-hero">
    <div class="wrap dp-hero-grid">
      <div>
        <p class="meta kicker">The signature service</p>
        <h1>Dave Perfect</h1>
        <p class="lede">A named service, not a slogan. Coined in our own shop, named after our founder, and asked for by name by our clients.</p>
      </div>
      <img class="dp-hero-seal" src="/brand/seal-green.svg" alt="Dave Perfect seal, Amárach Net Solutions" width="200" height="200">
    </div>
  </div>
  <section class="section" style="padding-top: calc(var(--section) * 0.3);">
    <div class="wrap">
      <div class="prose">
        <p>A new computer out of the box is not ready to work. It ships loaded with trial software, promotional apps, and startup items that run whether or not anyone wants them. An older machine has the same problem from the other direction: years of half-removed programs, browser add-ons, and background services that accumulated one install at a time.</p>
        <p>Both feel slow for the same reason: <strong>the machine is busy doing things nobody asked for.</strong></p>
        <p>Dave Perfect is the setup and cleanup pass that fixes that. It's the standard every machine we deliver meets before it reaches your desk, and the treatment that brings an existing machine back.</p>
        <h2>What's in the pass</h2>
        <ol class="dp-steps">
        {steps_html}
        </ol>
        <blockquote>"You don't need a new machine with more memory and a faster processor. You just need to be Dave Perfect."</blockquote>
        <p>Available on new equipment, on existing machines that have slowed down, and on a schedule for offices that would rather not think about it.</p>
      </div>
    </div>
  </section>
  <section class="section section--navy closing">
    <div class="wrap">
      <p>Got a machine that's slower than it should be?</p>
      <a class="phone-big" href="{TEL}">Call {PHONE}</a>
    </div>
  </section>
"""
    out = ROOT / "dave-perfect" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell("Dave Perfect | Amárach Net Solutions",
                         "Dave Perfect is Amárach's signature setup and cleanup service: the pass that makes a machine faster, quieter, and calmer, on new equipment and old.",
                         body, "/dave-perfect/"))


def build_about():
    body = f"""
  <div class="page-hero">
    <div class="wrap">
      <p class="meta kicker">About</p>
      <h1>Amárach Net Solutions</h1>
      <p class="lede">An independent IT firm in Rockford, Illinois, founded in 1997 and built on long client relationships.</p>
    </div>
  </div>
  <section class="section" style="padding-top: calc(var(--section) * 0.3);">
    <div class="wrap contact-grid">
      <div style="max-width: 340px;">
        <picture>
          <source srcset="/assets/dave-about.webp" type="image/webp">
          <img src="/assets/dave-about.jpg" alt="David Lickteig, founder of Amárach Net Solutions" width="800" height="800" style="border-radius: var(--radius); box-shadow: var(--shadow);">
        </picture>
        <p class="meta" style="margin-top: 14px; color: var(--blue);">David JP Lickteig &middot; Founder</p>
      </div>
      <div class="prose">
        <p>Amárach Net Solutions was founded by David Lickteig in 1997, and has been serving Rockford-area businesses ever since. The model hasn't changed in twenty-nine years: senior-level work, direct relationships, and networks the firm knows well because it built them.</p>
        <p>Dave is a Microsoft Certified Professional. Before founding Amárach, he served as Assistant Network Administrator for the City of Rockford at the Rockford Public Library, and before computers, spent eleven years in industrial sales calling on manufacturers across Winnebago County. It's a useful background for explaining a server to someone who doesn't want to hear about a server. He studied at Iowa State University.</p>
        <h2>How we work</h2>
        <p>Clients range from one-person shops to companies with more than a hundred employees: dental and medical offices, professional firms, manufacturers, nonprofits. Some have been with the firm for decades. Most are within an hour of Rockford; some are further out and work with us entirely remotely.</p>
        <p>There's no ticket queue and no tier-one script. The person working on your network is the one who set it up, knows its history, and remembers what was done last time. That continuity is the product.</p>
        <p><a href="/contact/">Get in touch &rarr;</a></p>
      </div>
    </div>
  </section>
"""
    out = ROOT / "about" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell("About | Amárach Net Solutions",
                         "Amárach Net Solutions is an independent IT firm in Rockford, Illinois, founded by David Lickteig in 1997.",
                         body, "/about/"))


def build_contact():
    body = f"""
  <div class="page-hero">
    <div class="wrap">
      <p class="meta kicker">Contact</p>
      <h1>Talk to us</h1>
      <p class="lede">The fastest way is the phone. If it's not urgent, the form works too, and we'll get back to you within one business day.</p>
    </div>
  </div>
  <section class="section" style="padding-top: calc(var(--section) * 0.3);">
    <div class="wrap contact-grid">
      <div>
        <a class="contact-phone" href="{TEL}">{PHONE}</a>
        <ul class="contact-facts">
          <li><span class="meta">Email</span><a href="mailto:davidjp@amarach.net">davidjp@amarach.net</a></li>
          <li><span class="meta">Service area</span>On-site across the Rockford region and northern Illinois. Remote support and managed care of computers and servers, anywhere.</li>
          <li><span class="meta">Hours</span>[[HOURS]]</li>
        </ul>
      </div>
      <form method="POST" action="/api/contact" class="contact-form">
        <div class="form-grid">
          <div>
            <label for="cf-name">Name</label>
            <input id="cf-name" name="name" autocomplete="name" required>
          </div>
          <div>
            <label for="cf-business">Business</label>
            <input id="cf-business" name="business" autocomplete="organization">
          </div>
          <div>
            <label for="cf-phone">Phone</label>
            <input id="cf-phone" name="phone" type="tel" autocomplete="tel">
          </div>
          <div>
            <label for="cf-email">Email</label>
            <input id="cf-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="full">
            <label for="cf-message">What's going on?</label>
            <textarea id="cf-message" name="message" rows="5" required></textarea>
          </div>
          <div class="hp" aria-hidden="true">
            <label for="cf-website">Website</label>
            <input id="cf-website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <div class="full">
            <button class="btn btn--primary" type="submit">Send message</button>
          </div>
        </div>
      </form>
    </div>
  </section>
"""
    out = ROOT / "contact" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell("Contact | Amárach Net Solutions",
                         "Call 815-636-8311 or send a message. IT support for Rockford-area businesses, on-site and remote.",
                         body, "/contact/"))


if __name__ == "__main__":
    articles = build_knowledge()
    build_services()
    build_dave_perfect()
    build_about()
    build_contact()
    print(f"Built {len(articles)} articles + 4 section pages")
