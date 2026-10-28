# ASI Holidays - Phase 1

Django + PostgreSQL backend, React (Vite) frontend. Enquiry-first travel site.

## Upgrading an existing copy (you already ran the first starter)

1. Unzip this over your project folder and overwrite files.
2. In `backend/` (venv active): `python manage.py migrate`
   (old packages are converted automatically: category "india"/"international" moves to the new Region field)
3. Restart `runserver` and `npm run dev`.

## Run from scratch

Backend (Windows PowerShell shown; use `source .venv/bin/activate` on Mac/Linux):
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:USE_SQLITE="1"          # skip this line if you use Postgres (docker compose up -d)
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_sample # optional: 6 demo packages (python manage.py seed_sample --clear removes them)
python manage.py runserver
```
Frontend (second terminal):
```
cd frontend
copy .env.example .env
npm install
npm run dev
```
Site: http://localhost:5173  Admin: http://localhost:8000/admin/

## First things to do in the admin
1. **Site settings**: WhatsApp number (digits with country code, e.g. 919876543210), phone, email, address, opening hours, "response time" (shown on the Thank-you page), about text, mission.
2. **Policy pages**: paste the client's Privacy, Terms and Cancellation text.
3. **Packages**: add real packages (Published = on the site, Featured = Popular packages on Home).
4. Put the client's logo at `frontend/public/logo.png` and an optional hero photo at `frontend/public/hero.jpg`.

## Phase 1 scope vs the UI designs

| Design screen | Status |
|---|---|
| Home (search, trust strip, holiday kinds, popular packages, WhatsApp band) | Built |
| Holiday packages (filters: where, trip type, food, travelling with) | Built |
| Package detail (itinerary, included, enquiry form, WhatsApp) | Built |
| About | Built |
| Contact (form, details, map, WhatsApp) | Built |
| Thank-you | Built |
| Policies | Built (client supplies text) |
| Mobile (menu, floating WhatsApp) | Built |
| Admin: packages, enquiries, status, follow-up notes, WhatsApp link per lead | Built (Django admin) |
| Email alert to team on new enquiry | Built (set ENQUIRY_NOTIFY_EMAILS) |
| WhatsApp click tracking + Google Analytics events | Built (set VITE_GA_ID) |
| Spam protection (honeypot + rate limit), consent required | Built |
| Home "Describe your trip" AI band, AI planner, quiz, group room, lead scoring, reply drafts | Phase 2, not built |
| Dashboard counter cards, Reports, SEO screens | Not built (Django admin lists and filters stand in) |

## API
- `GET /api/packages/?region=india,international&category=honeymoon,family&food=veg,jain&with=kids&featured=1`
  (region and category match ANY; food and with match ALL)
- `GET /api/packages/<slug>/`
- `POST /api/enquiries/`  `POST /api/whatsapp-click/`
- `GET /api/site/`  `GET /api/policies/`

## Before launch
- **SEO**: a client-rendered React app is weak for destination pages. Decide: Next.js, or prerender. Not solved here.
- Production env: `DJANGO_DEBUG=0`, real `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, SMTP settings, HTTPS, database backups.
- Serve uploaded images (MEDIA) from nginx or object storage; Django only serves them in debug.
- Email is sent inside the request. Fine at this volume; move to a background job if enquiries grow.

## Tests
`cd backend && python manage.py test`  (16 tests: filters, enquiry validation, consent, honeypot, email, site settings)
