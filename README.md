# Arunika — Flask Tech Service Website
**Bilingual (EN + casual ID) · Dark mode · Tailwind · Alpine.js**

---

## Folder Structure

```
techsite/
├── app.py                    # Flask app + routes + i18n logic
├── requirements.txt
├── translations/
│   ├── en.json               # English copy
│   └── id.json               # Casual Indonesian copy
├── templates/
│   ├── base.html             # Shared layout (header, footer, dark mode, lang toggle)
│   ├── home.html
│   ├── services.html
│   ├── why_us.html
│   ├── portfolio.html
│   └── contact.html
└── static/
    ├── css/                  # Optional custom CSS overrides
    ├── js/                   # Optional custom JS
    └── images/               # Project screenshots, icons
```

---

## Quick Start

```bash
pip install flask
python app.py
# Open http://localhost:5000
```

---

## Language Switching

Language is persisted via **cookie** (`lang=en` or `lang=id`).

- Toggle in header dropdown (top-right)
- Toggle in footer (visible buttons)
- Route: `GET /set-lang/<en|id>` — sets cookie, redirects back
- Optional subpath aliases: `/en/` and `/id/` also set cookie then redirect

### How translations load in Jinja2

```python
# In app.py — loaded once at startup
TRANSLATIONS = {}
for lang in ["en", "id"]:
    with open(f"translations/{lang}.json") as f:
        TRANSLATIONS[lang] = json.load(f)

# t() helper injected as context processor
def t(key_path):
    keys = key_path.split(".")
    data = TRANSLATIONS.get(g.lang, TRANSLATIONS["en"])
    for k in keys:
        data = data.get(k, key_path) if isinstance(data, dict) else key_path
    return data

@app.context_processor
def inject_globals():
    return {"t": t, "lang": g.lang, ...}
```

In templates: `{{ t('home.hero_headline') }}`

---

## Dark Mode

Implemented with Tailwind's `class` strategy + Alpine.js.

- `<html>` gets class `dark` when enabled
- All colors use CSS variables (`--c-bg`, `--c-surface`, `--c-text`, etc.)
- Light and dark values defined separately — **not** CSS `invert`
- Preference persisted to `localStorage` via Alpine's `$watch`
- Respects `prefers-color-scheme` on first visit

```html
<!-- html element -->
<html x-data="{ darkMode: ... }" :class="{ 'dark': darkMode }">

<!-- Toggle button -->
<button @click="darkMode = !darkMode">...</button>
```

---

## Color Palette

Non-mainstream, professional, forest-teal scheme:

| Token           | Light value | Dark value  |
|-----------------|-------------|-------------|
| Brand primary   | `#229478`   | `#3db394`   |
| Brand light     | `#6cccaf`   | `#6cccaf`   |
| Background      | `#f8faf9`   | `#0d1512`   |
| Surface         | `#ffffff`   | `#141f1b`   |
| Surface 2       | `#f0f4f2`   | `#1a2922`   |
| Border          | `#d8e4de`   | `#233028`   |
| Text            | `#0f1f1a`   | `#e8f2ee`   |
| Text muted      | `#4a6b5f`   | `#7aab96`   |

**Rationale**: Deep forest-teal avoids overused purple/blue. The dark mode uses near-black with a teal tint — feels premium without being harsh.

---

## Typography

| Role    | Font            | Rationale                              |
|---------|-----------------|----------------------------------------|
| Display | **Syne**        | Geometric, confident, slightly unusual |
| Body    | **DM Sans**     | Clean, readable, modern humanist       |
| Mono    | **JetBrains Mono** | Code/label accent, technical feel   |

---

## Branding Voice

**English**: Professional but approachable. Short sentences. Focus on outcomes.
- "We Build Digital Things That Actually Work"
- "No fluff. No jargon."

**Bahasa Indonesia (casual)**: Friendly, natural, idiomatic for young adults & UKM owners.
- Use contractions: "nggak", "biar", "buat", "bareng kamu"
- Short punchy CTAs: "Yuk Ngobrol", "Ayo Mulai", "Ceritain ke Kami"
- Avoid formal phrasing: NOT "Silakan menghubungi kami" → USE "Hubungi kami sekarang"
- Mirror English meaning, not word-for-word

---

## Accessibility & SEO

- `lang` attribute set on `<html>` per page language
- Semantic heading hierarchy (h1 → h2 → h3)
- All interactive elements have `aria-label`
- `alt` attributes on all `<img>` (add when using real images)
- Meta `title` and `description` localized per page via `t('meta.*')`
- `<nav aria-label="Main navigation">`
- Form labels explicitly associated with inputs via `for`/`id`

---

## QA Checklist — Bilingual Testing

### Content Parity
- [ ] All EN keys exist in id.json with no missing keys
- [ ] Every CTA button has both language versions
- [ ] Form labels, placeholders, validation messages translated
- [ ] Footer tagline and legal links translated
- [ ] Page titles (`<title>`) and meta descriptions translated

### Language Switching
- [ ] Header lang toggle works on every page
- [ ] Footer lang selector works on every page
- [ ] Cookie persists after browser refresh
- [ ] Redirects back to same page after switch
- [ ] `lang` attribute on `<html>` reflects current language

### Dark Mode
- [ ] Dark toggle works on all pages
- [ ] No inverted colors — colors are explicitly defined per mode
- [ ] `localStorage` persists across page navigations
- [ ] Respects `prefers-color-scheme` on first visit
- [ ] All cards, forms, nav, footer look correct in dark mode

### SEO Tags
- [ ] Unique `<title>` per page per language
- [ ] Unique `<meta name="description">` per page per language
- [ ] `<html lang="en|id">` correct

### Accessibility
- [ ] Keyboard navigation works (tab order logical)
- [ ] All buttons/links have descriptive labels
- [ ] Form errors visible and associated with correct inputs
- [ ] Contrast ratio ≥ 4.5:1 for body text in both modes
- [ ] Mobile nav usable on 320px width

### Forms
- [ ] Required field validation triggers for empty name/email/message
- [ ] Email format validation works
- [ ] Success state shown after valid submission
- [ ] Form data NOT lost on validation failure (values preserved)
- [ ] Indonesian validation messages shown when lang=id

---

## Extending: Adding a New Language

1. Create `translations/ms.json` (copy en.json, translate values)
2. Add `"ms"` to `SUPPORTED_LANGS` in `app.py`
3. The header/footer lang switchers will auto-render it

---

## Production Notes

- Replace `app.secret_key` with a real secret from env var
- Add email sending in the contact form handler (Flask-Mail or SMTP)
- Swap Tailwind CDN for compiled build: `npx tailwindcss -o static/css/main.css --minify`
- Add CSRF protection (Flask-WTF)
- Add rate limiting on `/contact` (Flask-Limiter)
