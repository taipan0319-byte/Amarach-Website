# Amárach Net Solutions — Website Build Spec

Hand this file to Claude Code as the source of truth. Build in the order given in §11.

---

## 1. Summary

Static marketing site plus a two-tier knowledge base for a one-person IT consultancy in Rockford, IL. Owner: David JP Lickteig, Microsoft Certified Professional, in business since 1997.

Audience: office managers, practice administrators, and owner-operators at small-to-midsize businesses — dental and medical practices, professional firms, light industrial, sole proprietors up to 100+ employee companies. These are not IT buyers. They are people whose computers are slow, whose server made a noise, or who just bought six new machines and need them set up. Write for them.

The site's single job: make a stranger comfortable enough to call, and give existing clients a place to self-serve.

Tone: plain, unhurried, specific. Twenty-nine years of doing this well. No "leverage," no "solutions-driven," no exclamation points outside of Dave's own quoted voice.

---

## 2. Still needed before launch

Placeholders are in the copy below as `[[BRACKETED]]` — search for them.

- `[[SERVICE_AREA]]` — how he describes the radius (e.g. "Rockford, Belvidere, Loves Park, Machesney Park, and the wider Rock River Valley")
- `[[HOURS]]` — and whether there's an after-hours/emergency path
- Two or three client testimonials, first name + business type + city is enough ("Karen M., dental practice, Belvidere")
- Confirm the Irish meaning and pronunciation of Amárach before it goes in print
- Decide: does Dave want to write KB articles in a browser, or in a text editor? This determines §7.

---

## 3. Architecture

**Build v1 as a fully public static site. No client login yet.**

Deferred by decision — the gated client area is out of scope for launch. Design for it anyway so it can be added later without a rebuild.

- **Site:** plain HTML/CSS/vanilla JS, or Astro if a build step helps generate the knowledge base index. No React, no SPA.
- **Host:** Cloudflare Pages (free) or Netlify (free). Git push deploys. Domain: **amarach.net**.
- **Knowledge base:** all articles public in v1. Keep the `public: true` frontmatter field anyway (§7) — when the client area is added, flipping an article to private becomes a one-word edit instead of a migration.
- **Leave the route free:** don't use `/clients` for anything else.

When the client area does get built, the recommended path is Cloudflare Access on `/clients/*` — free up to 50 users, one-time PIN by email, no passwords for Dave to store or reset.

Standing rule regardless of timing: a JavaScript password prompt on a static site is not security. If the browser can fetch the content, it is public. Client network documentation, license keys, and credentials must sit behind server-side gating or not be on the site at all. Do not build a fake login.

## 4. Site map

```
/                     Home
/services             What Dave does
/dave-perfect         The signature service — its own page
/knowledge            Knowledge base index (public articles)
/knowledge/<slug>     Individual article
/clients              RESERVED — not built in v1
/about                Dave, credentials, history
/contact              Phone, email, form, service area
```

Header on every page: wordmark left, nav center, phone number right as a `tel:` link. The phone number is the primary conversion on this site and must be visible without scrolling on every page, including mobile.

Footer: phone, email, service area, MCP credential, "Serving the Rock River Valley since 1997," KB link.

---

## 5. Design tokens

### Color

Derived from Dave's headshot — navy jacket, light blue shirt, cool gray seamless — so the photography and the interface look like one decision.

```css
--ink:        #14181F;  /* body text */
--navy:       #1B2A4A;  /* headers, footer, primary buttons */
--blue:       #3D6E9E;  /* links, active nav, icons */
--shirt:      #C9DCEF;  /* tints, table stripes, blockquote fills */
--paper:      #FFFFFF;  /* default page */
--band:       #F4F2EE;  /* alternating section bands */
--rule:       #DBD9D4;  /* hairlines, borders */
--seal:       #2F6F4E;  /* Dave Perfect seal ONLY — nowhere else */
```

Nine values, and the ninth is reserved. If a tenth color is needed, something has gone wrong.

### Type

One family, three roles: **IBM Plex** (Google Fonts, open license).

- **IBM Plex Serif** — h1, h2, and pull quotes. Weight 600. Gives the age-and-competence register without drifting into decorative.
- **IBM Plex Sans** — all body, nav, UI. 400 and 500. Body at 18px / 1.65.
- **IBM Plex Mono** — file paths, registry keys, commands, KB metadata labels. Small caps-ish at 13px, letterspaced 0.04em.

Why this rather than a fashionable serif-plus-grotesk pairing: KB articles for an IT practice will be full of paths like `C:\Users\...\AppData\Local\Temp` and service names. The mono face is load-bearing content, not decoration, so the family that ships a matched mono is the correct family. It also reads faintly of engineering documentation, which is exactly what Dave sells.

Scale: 44 / 32 / 24 / 18 / 15 / 13. Tighten h1 to 1.1 line-height and -0.01em tracking. No font sizes below 13px anywhere.

### Layout

- Max content width 1120px; article measure 68ch, hard limit. Long lines are the most common failure in KB pages.
- Section vertical rhythm: 96px desktop, 56px mobile. Alternate `--paper` and `--band`.
- Border radius 4px, uniform. Not 0 (harsh), not 16px (app-like).
- One shadow token only, very soft, for cards: `0 1px 3px rgba(20,24,31,.08)`.
- Motion: none beyond 150ms color transitions on hover/focus. Respect `prefers-reduced-motion`. Dave asked for no animation; honor that literally — restraint is the aesthetic here.

### Signature element

**The Dave Perfect seal.** Techs put a service sticker on a machine when it's been worked on. That's the artifact from Dave's own world, so it becomes the site's one memorable device: a small circular seal in `--seal` green, IBM Plex Mono letterforms running around the ring — `DAVE PERFECT · AMÁRACH NET SOLUTIONS` — with a date field in the center. Rendered as inline SVG.

It appears in exactly three places: the hero, the top of `/dave-perfect`, and as a favicon. Nowhere else. This is where all the boldness gets spent; everything else stays quiet.

---

## 6. Pages and copy

Copy below is ready to use. Edit freely — it's a floor, not a ceiling.

### Home

**Hero.** Headshot right (cropped per §9), text left. No background image, no gradient.

> # Perfect today. Ready for tomorrow.
>
> Amárach is the Irish word for *tomorrow*. Since 1997, David Lickteig has kept the computers, servers, and networks of Rockford-area businesses running quietly in the background — so the people using them can get on with the actual work.
>
> [ Call 815-636-8311 ]   [ See what we do ]

Under the hero, one line of quiet proof: `Microsoft Certified Professional · Independent since 1997 · On-site and remote`

**Three pillars.** Not numbered — these are parallel, not sequential, so numbering would lie about the content.

- **Networks that stay up.** Windows Server, workstations, backups, and the boring maintenance that prevents interesting problems.
- **Equipment, handled end to end.** Specified, sourced, provisioned, and delivered working. You don't research part numbers; you tell us what the job is.
- **Software that fits your field.** Dental, medical, and industry-specific systems — installed, integrated, and made to talk to everything else.

**Dave Perfect teaser.** Band background, seal on the left, this text on the right:

> ### Before your machine leaves the bench, it's Dave Perfect.
>
> A new computer out of the box is not ready to work. Neither is one that's been in service for four years. Dave Perfect is the setup and cleanup pass that makes a machine faster, quieter, and calmer — correct settings, correct drivers, nothing hidden running in the background eating memory you paid for.
>
> *"You don't need a new machine with more memory and a faster processor. You just need to be Dave Perfect."*
>
> [ What's in a Dave Perfect pass → ]

**Who we work with.** Plain prose, no logo wall (a solo consultancy with a logo wall looks borrowed):

> Clients range from one-person shops to companies with more than a hundred employees. Dental and medical offices, professional firms, manufacturers, nonprofits. Most are within an hour of Rockford; some are further out and work with us entirely remotely.

**Testimonials** — two, plain text with a hairline above. Omit the section entirely until real ones exist. Never invent them.

**Closing CTA.** Navy band, phone number large, one line: `Something slow, broken, or overdue for replacement? Call 815-636-8311.`

### Services

Intro: *One person, accountable, who has seen your problem before.*

Then five sections, each a short paragraph and a plain bulleted list. No icons — or if icons, one consistent thin-line set, never emoji.

1. **Network administration** — Windows Server, Active Directory, file and print, permissions, remote access, patching, backup verification, monitoring. The recurring work that keeps the interesting failures from happening.
2. **Equipment acquisition and provisioning** — spec'ing hardware to the actual job, sourcing at fair cost, imaging, migration of files and settings, disposal of the old unit. Every new machine arrives Dave Perfect.
3. **Vertical software integration** — practice management, imaging, ERP, and other field-specific systems: installation, updates, vendor coordination, and making them work with the rest of your network. Includes being the person who sits on hold with the software vendor so you don't have to.
4. **Diagnosis and troubleshooting** — figuring out what is actually wrong. Intermittent faults, slow performance, printing, email, connectivity, mystery noises. Twenty-nine years of pattern recognition.
5. **Support, on-site and remote** — routine help for staff, one-off emergencies, and standing arrangements. Remote sessions handle most issues within the hour; when it needs hands, Rockford is a short drive.

Close with a note on how engagement works — hourly, project, or ongoing — as soon as Dave confirms which he offers.

### Dave Perfect

Seal at top. Then:

> # Dave Perfect
>
> A named service, not a slogan. Coined in our own shop, named after the man who does it, and asked for by name by our clients.

Explain the problem plainly: new machines ship loaded with trial software and startup items; older machines accumulate years of half-removed programs, browser add-ons, and background services. Both feel slow for the same reason — the machine is busy doing things nobody asked for.

Then the pass itself, as a checklist. This *is* a sequence, so numbering is honest here:

1. Inventory and baseline — what's installed, what's running, what's actually using the resources
2. Remove bundled trials, redundant utilities, and unnecessary startup items
3. Correct system and registry settings for how the machine will really be used
4. Current drivers, firmware, and updates — then verified, not assumed
5. Security and backup confirmed working
6. Files, settings, and profiles migrated if it's a replacement
7. Line-of-business and vertical software installed and tested
8. Final pass: thermals, noise, boot time, and a real-world speed check

Close with the quote, set as a pull quote in Plex Serif, and a line: *Available on new equipment, on existing machines that have slowed down, and on a schedule for offices that would rather not think about it.*

### Knowledge

Public index. Intro one line: *Fixes, explanations, and answers to the questions we get most. Free to read, no login.*

Category filter as plain links, not a dropdown. Article cards: title, one-sentence summary, category, date in mono. Newest first.

Categories: **Getting Started**, **Troubleshooting**, **Security & Backups**, **Hardware**, **Email & Internet**, **FAQ**.

Seed with six to eight real articles before launch. Empty knowledge bases read worse than no knowledge base. Suggested first articles, all drawn from things Dave certainly answers weekly:

- Why your computer got slower, and what actually fixes it
- What we need from you before we set up a new machine
- Is your backup actually working? Three things to check
- How to tell a real Microsoft warning from a fake one
- When to repair and when to replace
- How remote support sessions work

Article template: h1, mono metadata line (category · updated date · read time), 68ch measure, real subheadings, code and paths in Plex Mono with a `--band` background. At the foot of every article: *Still stuck? Call 815-636-8311.*

### Clients

Not built in v1. Reserve the route and leave it out of the nav entirely — an empty or "coming soon" page is worse than no page.

### About

Photo on white here (second crop, §9). Then Dave in first person if he'll write it, third person if not. Facts available: independent since 1997, Microsoft Certified Professional, Assistant Network Administrator for the City of Rockford (Rockford Public Library) 1998–2000, eleven years in industrial sales before that, Iowa State University.

The industrial sales history is a real asset, not filler — it's why he can talk to a shop owner without condescending. Use it: *Before computers, eleven years calling on manufacturers across Winnebago County. It's a useful background for explaining a server to someone who doesn't want to hear about a server.*

### Contact

Phone large and first. Email. Service area. Hours. Then a short form: name, business, phone, email, one message field. Six fields maximum.

Form handling on a static host: Cloudflare Pages Functions, Netlify Forms, or Formspree. Include honeypot, no CAPTCHA. Success state replaces the form with a real confirmation naming the next step and the phone number — not just "Thanks!"

---

## 7. Knowledge base format

Assuming Dave is comfortable in a text editor — reasonable for a Microsoft Certified Professional, but confirm.

Flat Markdown in `/content/knowledge/`, one file per article:

```markdown
---
title: Why your computer got slower, and what actually fixes it
category: Troubleshooting
summary: Slowness is usually background clutter, not a hardware limit.
date: 2026-07-24
public: true
---

Body in Markdown.
```

Index page is generated from frontmatter. Adding an article = adding a file. `public: false` routes it to the client area instead.

If Dave wants browser-based authoring, the honest options are (a) real WordPress, (b) a static site plus a git-backed CMS like Decap, or (c) he emails articles and someone commits them. Present the tradeoffs; don't pick for him.

---

## 8. Logo

Directions are drawn and rendered in `amarach-logo-concepts.html`. Recommended: the horizon lockup for the company, the service seal for Dave Perfect. Detail below.

Wordmark, not an icon lockup. Small IT firms with abstract swoosh marks look like every other small IT firm.

- **AMÁRACH** in IBM Plex Serif 600, letterspaced 0.06em. Keep the fada on the á — it's correct Irish and it's a distinguishing detail.
- **NET SOLUTIONS** beneath in Plex Sans 500, 0.16em tracking, sized to the wordmark's width.
- Color: `--navy`. Single-color reversed version in white for the footer.

Optional mark, only if Dave wants one: a thin horizontal rule beneath the wordmark with a shallow arc rising from its left third — a horizon and the first curve of a sunrise. It plays *tomorrow* without becoming a globe or a swoosh. One weight, no gradient.

Deliver as SVG: full lockup, stacked, horizontal, reversed, and favicon (which uses the seal, not the wordmark).

---

## 9. Photograph

The supplied headshot is a proper studio shot — soft directional light, cool gray seamless, navy jacket. No background removal needed or wanted; the existing background is an asset.

Two derivatives with Pillow:

- **Hero:** crop to 4:5 portrait, chest-up, eyes at roughly 38% from the top. Shift the crop slightly toward his left so he faces into the text column. Export at 1200px wide, WebP with JPEG fallback.
- **About:** 1:1 square, slightly wider framing, background lifted to near-white to sit on the white page. 800px.

Both need `alt="David Lickteig, owner of Amárach Net Solutions"`. Do not oversharpen, do not add a border, do not apply a duotone.

---

## 10. Quality floor

Not optional, not announced on the page.

- Responsive to 360px. Test the nav and the phone link at that width first, not last.
- Visible keyboard focus rings on every interactive element. Do not remove outlines.
- Real semantic HTML: one h1 per page, headings in order, `<nav>`, `<main>`, `<footer>`.
- Contrast: everything passes WCAG AA. Check `--blue` on `--band` specifically.
- `prefers-reduced-motion` respected.
- Page weight under 500KB on Home including the photo. Self-host the Plex fonts as woff2, subset Latin, two weights per face — do not link Google's CDN.
- Meta description and Open Graph tags per page. `LocalBusiness` JSON-LD on Home with the real phone, address, and service area — this matters more than anything else on the page for a Rockford business.
- No analytics beyond Cloudflare's built-in, unless Dave asks.

## 11. Build order

1. Confirm the §7 authoring decision with Dave. Architecture is settled: public static site, no login in v1.
2. Tokens and base stylesheet. Fonts self-hosted. Get type and spacing right before any page exists.
3. Header, footer, and one interior page shell.
4. Home.
5. Dave Perfect, including the SVG seal.
6. Services, About, Contact with working form.
7. Knowledge base: template, index generation, six seed articles.
9. Logo SVG set and favicon.
10. Photo derivatives.
11. Full pass: mobile, keyboard, contrast, weight, JSON-LD, then screenshot every page at 360px and 1440px and critique.

---

## 12. Competitive reference — what to take from the exemplars

Three sites reviewed: uscloud.com, trustedtechteam.com, kizan.com.

All three are enterprise Microsoft partners: hundreds of engineers, Fortune 500
clients, $500M revenue in one case. Amárach is one man with twenty-nine years of
clients. **Copying their playbook would actively damage credibility** — a solo
consultancy with a Fortune 500 logo wall and a "7,500+ customers" counter reads
as fabricated, because it would be. Take the structural patterns, leave the
scale signals.

### Take

**1. The homepage FAQ block.** US Cloud answers nine plain questions right on the
home page — who they are, can they really do this, what about X. It pre-empts
objections and it is excellent for search. Dave's version, in his own voice:
*Do you work with businesses my size? What does it cost? Do you have to come
on-site? What if my software vendor needs to be involved? How fast can you get
here?* Six to eight of these, below the services section.

**2. Specific numbers instead of adjectives.** These sites don't say "fast" —
they say fifteen-minute response, 85% resolved in-house, five-minute average.
Dave should publish two or three of his own **real** figures. Candidates: years
in business, typical response time, share of issues resolved remotely without a
visit, longest-running client relationship. That last one is his best statistic
and none of these firms can touch it. Do not invent or round generously; a
number a client could contradict is worse than no number.

**3. The comparison table.** US Cloud runs a feature grid against Microsoft and
resellers. Dave's version is stronger because his competitors are worse: the
big-box store service counter, the national MSP with a ticket queue, and the
owner's nephew. Rows: who actually shows up, do you get the same person twice,
does anyone know your network already, on-site availability, what happens at
7am when nothing boots. Keep it factual and unsmug — it should read as helping
someone choose, not as trash talk.

**4. A useful tool.** TrustedTech's server licensing calculators exist to earn
links and capture people mid-decision. Dave's equivalent, and it's a good one:
**a repair-or-replace estimator.** Age of machine, symptoms, what it's used for,
out comes a plain recommendation. It's the question he answers weekly, it's
genuinely useful, and it's the kind of page other local sites link to. Phase two,
after launch.

**5. Testimonials with a name, a title, and an edge.** The best line on any of
the three is a KiZAN client saying they tell you what you don't want to hear —
that they're honest brokers. That's persuasive because it isn't flattering.
When asking Dave's clients, ask for the specific thing he did, not for praise.

**6. Vertical segmentation.** KiZAN splits by industry: healthcare, financial,
manufacturing, professional. Dave has real verticals — dental, medical,
professional firms, light industrial. Don't build six pages; write one short
paragraph per vertical on the Services page naming the systems he actually
supports in each. Specific software names are what convince a practice manager,
and they're strong local search terms.

**7. Phone in the header, always.** All three do this. Confirms §4.

### Leave

- **Logo walls.** Not available and not appropriate.
- **Giant stat counters.** Impressive at 7,500 customers, sad at 40.
- **Mega-nav.** US Cloud has six dropdowns with fifty-plus links. Dave has five
  pages. A small firm imitating enterprise navigation looks like a small firm
  imitating enterprise navigation.
- **Autoplaying hero video.**
- **Corporate abstraction.** "Digitally transform employee experiences,"
  "aligning technology with business intent." Dave's reader manages a dental
  office and her scanner won't scan.
- **Emoji checkmarks in the hero.** TrustedTech does this; it reads cheap.
- **The tag-manager, consent-banner, chat-widget stack.** All three are heavy
  WordPress/HubSpot/Shopify builds. This is the single clearest argument for the
  static approach in §3 — Amárach's site can load in under a second on a phone
  in a parking lot, and none of theirs will.

### The positioning this points to

These firms all sell the same thing: scale, certifications, and a support
organisation. Dave cannot compete on any of it, and shouldn't try.

What he sells is the exact inverse — **the same person every time, who already
knows your network.** No ticket queue, no offshore tier-one, no account manager
turnover, no re-explaining your setup to a stranger. US Cloud's own marketing
argues that dedicated senior engineers beat a support pool; Dave *is* that
argument, taken to its limit. The site should say so plainly and early, ideally
in the first two lines of the home page, and everything else should follow from
it.
