import json

from django.conf import settings


class AIUnavailable(Exception):
    pass


def available():
    return bool(settings.ANTHROPIC_API_KEY)


def complete(system, user, model=None, max_tokens=1200):
    if not available():
        raise AIUnavailable("ANTHROPIC_API_KEY is not set")
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY, timeout=30)
    resp = client.messages.create(
        model=model or settings.ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def complete_json(system, user, model=None, max_tokens=1200):
    text = complete(system + "\n\nReply with one JSON object only. No markdown, no commentary.", user, model, max_tokens)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model did not return JSON")
    return json.loads(text[start : end + 1])