import logging
import re

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from packages.models import Package
from packages.serializers import PackageListSerializer

from . import client
from .services import RULES, STOP, _dump, catalogue

logger = logging.getLogger(__name__)

SYSTEM_SEARCH = RULES + """
A visitor searches for a holiday by feeling inside <search>. The only packages you may return are in <catalogue>.
They may write in any language and may not know place names (for example "relaxing" or "somewhere for my parents").
Return JSON with:
- intro: one friendly sentence in the visitor's language
- matches: up to 6 objects {"slug": copied exactly from the catalogue, "reason": one sentence in the visitor's language}, best first
Do not decide anything about budget. Return an empty matches list if nothing fits."""

EXTRA_STOP = {"something", "somewhere", "holiday", "holidays", "kind", "like", "place", "places"}
SYNONYMS = {  # feelings -> the words used in package moods and tags
    "relaxing": "relax", "relaxed": "relax", "calm": "relax", "peaceful": "relax", "beach": "relax", "resort": "relax", "unwind": "relax",
    "trek": "adventure", "trekking": "adventure", "safari": "adventure", "thrill": "adventure", "adventurous": "adventure", "hiking": "adventure",
    "parents": "seniors", "elders": "seniors", "grandparents": "seniors", "senior": "seniors",
    "children": "kids", "kid": "kids", "child": "kids",
    "heritage": "culture", "history": "culture", "food": "culture", "temple": "culture", "temples": "culture",
}


def inr(n):
    """₹1,00,000 style."""
    s = str(int(n))
    if len(s) <= 3:
        return "₹" + s
    head, tail, parts = s[:-3], s[-3:], []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail])


def _words(text):
    words = [w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP and w not in EXTRA_STOP and len(w) > 2]
    return list(dict.fromkeys(words + [SYNONYMS[w] for w in words if w in SYNONYMS]))


def keyword_rank(query, cat):
    """Used when AI is off or fails. Works for English words only."""
    words = _words(query)
    scored = []
    for c in cat:
        hay = " ".join([c["title"], c["destination"], c["summary"], c["region"], c["type"], c["moods"], *c["food"], *c["good_for"]]).lower()
        hits = [w for w in words if w in hay]
        if hits:
            scored.append((len(hits), c["slug"], hits))
    scored.sort(key=lambda x: -x[0])
    return [(slug, "Matches your search: " + ", ".join(hits)) for _, slug, hits in scored]


def search(query, budget, request=None):
    """All price and budget decisions are made here in code. The AI only judges relevance."""
    query = (query or "").strip()[:300]
    cat = catalogue()
    info = {c["slug"]: c for c in cat}
    price = {s: c["price_from_inr"] for s, c in info.items()}
    picks, intro, ai_ok = [], "", False

    if query and cat:
        if client.available():
            try:
                data = client.complete_json(SYSTEM_SEARCH, f"<catalogue>{_dump(cat)}</catalogue>\n<search>{query}</search>")
                intro = str(data.get("intro", ""))[:400]
                picks = [(m["slug"], str(m.get("reason", ""))[:300]) for m in data.get("matches", [])[:6] if m.get("slug") in info]
                ai_ok = True
            except Exception:
                logger.exception("AI search failed")
        if not ai_ok:
            picks = keyword_rank(query, cat)[:6]
    seen = set()
    picks = [p for p in picks if not (p[0] in seen or seen.add(p[0]))]

    budget_info, alternatives = None, []
    if budget:
        ok = lambda s: price[s] <= budget  # noqa: E731
        tight, note = False, ""
        if picks:
            fits = [p for p in picks if ok(p[0])]
            picks = fits + [p for p in picks if not ok(p[0])]
            if not fits:
                tight = True
                taken = {p[0] for p in picks}
                alternatives = [(s, f"Within your budget at {inr(price[s])} per person")
                                for s in sorted((s for s in info if ok(s) and s not in taken), key=lambda s: -price[s])[:3]]
                lowest = inr(min(price[s] for s, _ in picks))
                note = (f"The packages that match start at {lowest} per person, above your budget of {inr(budget)}. "
                        + ("Here are options within your budget. Ask a consultant about off-season dates that may lower the price."
                           if alternatives else "Tell a consultant your plan; they may be able to build a cheaper itinerary."))
        else:
            within = sorted((s for s in info if ok(s)), key=lambda s: -price[s])
            picks = [(s, f"Fits your budget at {inr(price[s])} per person") for s in within[:6]]
            if picks:
                if query:
                    intro = intro or "We could not match your words exactly, but these packages fit your budget."
            elif info:
                tight = True
                alternatives = [(s, f"Our lowest price: {inr(price[s])} per person") for s in sorted(info, key=lambda s: price[s])[:3]]
                note = (f"Our packages start at {inr(min(price.values()))} per person, above your budget of {inr(budget)}. "
                        "Tell a consultant your plan; they may be able to build a cheaper itinerary.")
        budget_info = {"amount": budget, "tight": tight, "note": note, "alternatives": alternatives}

    wanted = {s for s, _ in picks} | {s for s, _ in alternatives}
    pkgs = {p.slug: p for p in Package.objects.filter(slug__in=wanted, is_published=True)}

    def shape(items):
        return [{
            "package": PackageListSerializer(pkgs[s], context={"request": request}).data,
            "reason": reason,
            "within_budget": (price[s] <= budget) if budget else None,
        } for s, reason in items if s in pkgs]

    matches = shape(picks)
    if budget_info:
        budget_info["alternatives"] = shape(alternatives)
    if not intro:
        intro = ("These approved ASI Holidays packages match your search. A consultant confirms every quote." if matches
                 else "We could not find an exact match. Tell us what you want on WhatsApp and a consultant will help.")
    return {"intro": intro, "matches": matches, "budget": budget_info, "ai": ai_ok}


class SearchView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "search"

    def post(self, request):
        query = str(request.data.get("query") or "").strip()
        raw = request.data.get("budget")
        errors, budget = {}, None
        if raw not in (None, ""):
            try:
                budget = int(raw)
                if not 1000 <= budget <= 10_000_000:
                    errors["budget"] = ["Choose a budget between ₹1,000 and ₹1,00,00,000 per person."]
            except (TypeError, ValueError):
                errors["budget"] = ["Budget must be a number."]
        if len(query) > 300:
            errors["query"] = ["Keep your search under 300 characters."]
        if not query and budget is None and not errors:
            errors["query"] = ["Type what you are looking for or choose a budget."]
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(search(query, budget, request))