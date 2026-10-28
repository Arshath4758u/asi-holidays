MOODS = {
    "relax": {"title": "The Beach Unwinder", "line": "You travel to slow down: sea views, good food and nowhere to be."},
    "adventure": {"title": "The Trail Seeker", "line": "You want sunrise treks, new terrain and stories to tell."},
    "family": {"title": "The Family Connector", "line": "Your best trips are the ones everyone remembers together."},
    "culture": {"title": "The Culture Explorer", "line": "You travel for history, street food and the people you meet."},
}


def _q(i, text, relax, adventure, family, culture):
    return {"id": i, "text": text, "options": [
        {"key": "relax", "label": relax}, {"key": "adventure", "label": adventure},
        {"key": "family", "label": family}, {"key": "culture", "label": culture},
    ]}


QUESTIONS = [
    _q(1, "What kind of break do you want?", "Relaxing beach and resort", "Adventure and trekking", "Family time", "Culture and food"),
    _q(2, "Your perfect morning?", "Slow breakfast by the water", "Sunrise trek or safari", "Everyone around one big table", "Wandering old streets"),
    _q(3, "Pick a souvenir.", "A seashell from the shore", "A trail badge", "A group photo frame", "Local handicrafts"),
    _q(4, "How do you like your days planned?", "Almost nothing planned", "Packed with activities", "Easy for kids and elders", "Guided and informative"),
    _q(5, "Choose an evening.", "Sunset and a quiet dinner", "Campfire stories", "Games with the family", "A local food walk"),
]


def score(answers):
    """Most frequent mood wins. A tie goes to the mood chosen first."""
    counts = {}
    for a in answers:
        counts[a] = counts.get(a, 0) + 1
    best = max(counts.values())
    return next(a for a in answers if counts[a] == best)