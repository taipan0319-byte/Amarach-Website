# Start here

Everything needed to build amarach.net is in this folder.

```
amarach-build-spec.md    the full brief — read this first
brand/                   logo and seal, SVG masters + PNG previews
brand/README.md          usage rules, colours, minimum sizes
assets/                  Dave's headshot, uncropped
```

## First prompt to give Claude Code

Paste this once you've opened a terminal in this folder and run `claude`:

> Read amarach-build-spec.md in full, then brand/README.md. It's the complete
> brief for a static marketing site for a one-person IT consultancy.
>
> Before writing any code, tell me: your plan for the file structure, anything
> in the spec you think is a mistake, and any question you need answered. Then
> stop and wait. Don't start building until I say go.
>
> Two things to know: section 11 has the build order, and section 3 is settled —
> public static site, no login in v1.

Making it plan first and stop is worth the extra turn. It'll catch things and
you'll spend fewer tokens than you would unwinding a wrong start.

## Then, roughly in this order

1. Tokens and base stylesheet — get type and spacing right before any page exists
2. Header, footer, one page shell
3. Home
4. Dave Perfect
5. Services, About, Contact
6. Knowledge base template plus seed articles
7. Photo crops, favicon, final mobile and accessibility pass

Build one at a time and look at each before moving on. Claude Code will happily
produce all seven pages in one go, and then you're reviewing 2,000 lines at once.

## Two placeholders still in the spec

`[[SERVICE_AREA]]` and `[[HOURS]]`. Search for the double brackets. Everything
else — phone, email, domain — is filled in.

## Don't let it

- Add a JavaScript login. The spec explains why; it isn't security.
- Recreate the logo by typing AMÁRACH in a font. Use the SVG files.
- Close up the hairline gap where the beam crosses the A. It's deliberate.
- Invent testimonials, client names, or statistics. Every number on the site has
  to be one Dave can stand behind.
