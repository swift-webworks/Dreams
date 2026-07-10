# Dreams Tours and Travels — Django Website

Premium, SEO-optimized website for **Dreams Tours and Travels**, Rameswaram, Tamil Nadu.
Built with Django 5, Bootstrap 5.3, vanilla JS, and AOS animations — no React/Vue/jQuery.

---

## 1. Tech Stack

- Django 5.x
- SQLite (dev) / PostgreSQL (recommended for production, via `DATABASE_URL`)
- Bootstrap 5.3 + Bootstrap Icons (CDN)
- AOS (Animate On Scroll) for reveal animations (CDN)
- WhiteNoise for compressed static file serving
- Vanilla JavaScript only

## 2. Project Structure

```
dreams_tours/
├── manage.py
├── requirements.txt
├── .env.example
├── dreams_tours/          # Project settings, urls, wsgi/asgi
├── core/                  # Main app: models, views, admin, forms, urls
│   ├── models.py          # Vehicle, Destination, Story, Memory, ClientReview, ContactSubmission
│   ├── admin.py           # Admin panel config with image previews
│   ├── views.py           # All page views + robots.txt
│   ├── forms.py           # Contact form with honeypot + validation
│   ├── sitemaps.py        # XML sitemap for SEO
│   ├── context_processors.py  # Global company info (phone, address, map)
│   └── management/commands/seed_data.py  # Sample data loader
├── templates/
│   ├── base.html          # Navbar, footer, SEO meta, structured data
│   └── core/               # home, fleet_list, destination_list/detail, story, contact
└── static/
    ├── css/style.css      # Full design system (custom, not default Bootstrap look)
    └── js/main.js         # Navbar scroll, AOS init, fleet tier switch, counters
```

## 3. Local Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit values, especially DJANGO_SECRET_KEY
export DJANGO_DEBUG=True         # for local development only

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data       # optional: loads sample fleet/destinations/story/reviews
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` for the content dashboard.

## 4. Adding Real Content (Admin Panel)

Everything editable lives in Django Admin (`/admin/`):

- **Fleet → Vehicle**: name, category, tier (Budget/Premium), price/km, seats, image, "Featured" flag (max 3 shown on Home).
- **Destinations**: name, image, description, best time/season, travel type, "Featured" flag, optional custom meta title/description.
- **Our Story — Profiles**: one "Owner Introduction" entry + multiple "Staff Timeline" entries (auto-alternating layout).
- **Memories Gallery**: photos for the infinite-scrolling home section.
- **Client Stories — Reviews**: reviewer name/photo, star rating, review text, Google review link.
- **Contact Enquiries**: read-only log of form submissions (name, phone, destination, dates, member count).

## 5. Required Real Assets Before Launch

Replace these placeholders in `static/img/` and `static/video/`:

| File | Purpose | Recommended size |
|---|---|---|
| `static/video/hero-placeholder.mp4` | Hero background video | 1080p, muted, < 6MB, H.264 |
| `static/img/hero-poster.jpg` | Hero fallback poster | 1920×1080 |
| `static/img/og-cover.jpg` | Social share preview | 1200×630 |
| `static/img/vehicle-placeholder.jpg` | Fallback vehicle image | 1200×800 |
| `static/img/destination-placeholder.jpg` | Fallback destination image | 1200×900 |

All content images (fleet, destinations, story, memories, reviews) are uploaded through the Admin panel — convert to WebP/JPG and compress before upload for best Lighthouse scores.

## 6. SEO Checklist (Implemented)

- Unique meta title/description per page and per destination (auto-generated, or set manually in Admin)
- Canonical URLs, Open Graph tags, Twitter Cards on every page
- `robots.txt` and `sitemap.xml` generated dynamically (`core/views.py`, `core/sitemaps.py`)
- Structured data: `TravelAgency`/Local Business schema (site-wide), `BreadcrumbList` (destination pages), `FAQPage` (home)
- One `<h1>` per page, semantic HTML, descriptive `alt` text on every image
- Lazy loading (`loading="lazy"`) on all content images; hero video uses `preload`-friendly poster

> To finish SEO setup: verify the site in **Google Search Console** and submit `https://yourdomain/sitemap.xml`.

## 7. Performance Checklist (Implemented)

- WhiteNoise `CompressedManifestStaticFilesStorage` — gzip/Brotli + cache-busted filenames
- Google Fonts loaded with `preconnect` + non-blocking `media="print" onload` swap trick
- `font-display: swap` via Google Fonts CSS2 API
- CSS/JS separated into single cached files (no inline blocking scripts); scripts loaded with `defer`
- Images should be exported as WebP/compressed JPG with explicit `width`/`height` to prevent layout shift

**Before going live**, also run:
```bash
python manage.py collectstatic --noinput
```
and configure your web server (Nginx) to serve `/static/` and `/media/` directly with long cache headers.

## 8. Security Checklist (Implemented)

- CSRF protection on all forms (Django default + explicit token in contact form)
- Honeypot field (`website`) + IP-based rate limiting (5 submissions/hour) on the contact form
- Server-side phone number validation (Indian 10-digit format)
- Security headers via `SecurityMiddleware`: `X-Content-Type-Options`, `X-Frame-Options: DENY`, HSTS (production)
- `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` enabled when `DEBUG=False`
- **No secrets in source code** — `SECRET_KEY`, allowed hosts, database URL, email credentials all read from environment variables (`.env`)
- `ContactSubmission` records are read-only in Admin (no accidental edits/spoofing)

## 9. Accessibility Checklist (Implemented)

- Skip-to-content link, semantic `<nav>`, `<main>`, `<footer>`, `<address>`
- ARIA labels on icon-only buttons/links, `aria-current="page"` in breadcrumbs
- Visible focus states (`:focus-visible`) with high-contrast outline
- Form labels explicitly associated with inputs; error messages shown inline
- Sufficient color contrast using the primary palette on light backgrounds

## 10. Deployment (Production)

### Option A — VPS / Ubuntu with Gunicorn + Nginx

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn dreams_tours.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Point Nginx at Gunicorn (proxy_pass to `127.0.0.1:8000`), serve `/static/` and `/media/` directly from disk, and terminate SSL with a free Let's Encrypt certificate. Set all variables from `.env.example` in your server's environment (or a real `.env` file, `chmod 600`).

### Option B — PaaS (Railway / Render / PythonAnywhere)

1. Set environment variables from `.env.example` in the platform's dashboard.
2. Set `DATABASE_URL` to a managed Postgres instance (the project auto-detects it via `dj-database-url`).
3. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command: `gunicorn dreams_tours.wsgi:application`

### Post-Deploy Checklist

- [ ] Set a strong, random `DJANGO_SECRET_KEY`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Set correct `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`
- [ ] Replace placeholder images/video with real assets
- [ ] Update the Google Maps embed URL in `core/context_processors.py` with the real business location
- [ ] Run Google Lighthouse and confirm 95+ Performance/Accessibility, 100 SEO/Best Practices
- [ ] Submit sitemap to Google Search Console

---

*Default admin credentials created during setup (change immediately in production):*
`admin` / `DreamsAdmin@2026` — **do not use in production, this is for local testing only.**
