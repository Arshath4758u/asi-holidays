# ASI Holidays - Phase 1 starter

Django + PostgreSQL backend, React (Vite) frontend. Enquiry-first travel site.

## Run locally

### 1. Database
```
docker compose up -d
```
(No Docker? `USE_SQLITE=1` in the backend env skips Postgres for quick testing.)

### 2. Backend
```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then export the vars, or set them in your shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Admin: http://localhost:8000/admin/ (add packages, set Published, manage enquiries)

### 3. Frontend
```
cd frontend
cp .env.example .env        # set VITE_WHATSAPP_NUMBER
npm install
npm run dev
```
Site: http://localhost:5173 (Vite proxies /api and /media to Django)

## What is built

| Phase 1 item | Where |
|---|---|
| Package catalogue + detail pages | `backend/packages`, `frontend/src/pages` |
| Enquiry form (name, WhatsApp, destination, date, travellers, budget) | `backend/enquiries`, `EnquiryForm.jsx` |
| WhatsApp button with pre-filled message + click tracking | `WhatsAppButton.jsx`, `WhatsAppClick` model |
| Admin dashboard | Django admin (no code needed to edit packages, prices, enquiries, follow-up notes) |
| Spam protection | Honeypot field + DRF rate limits (10 enquiries/hour/IP) |
| No payment data stored | By design, none collected |

## Phase 2 hooks already in place
- `Enquiry.lead_score` (hot/warm/cold) is reserved for lead scoring.
- `Enquiry.consent_followup` records consent before follow-ups.
- Keep AI behind Django views (e.g. `backend/ai/`) so API keys stay server-side and only approved, published packages are ever suggested.

## Known gaps to decide before launch
1. **SEO:** a client-rendered React app is weak for destination-specific SEO, which the proposal promises. Options: move the frontend to Next.js, or prerender the package pages at build time. Decide this before Week 3.
2. Production: set `DJANGO_DEBUG=0`, a real `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, serve media from object storage or nginx, configure backups.
3. Policy pages (privacy, cancellation, terms) need client content.
4. Google Analytics / event tracking not wired yet.
5. Email/WhatsApp notification to the team on new enquiry not wired yet (admin list only).
