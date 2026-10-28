from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from packages.models import Package
from packages.serializers import PackageListSerializer

from . import quiz
from .models import Room, RoomOption, RoomVote


# ------------------------------------------------------------------ mood quiz
class QuizView(APIView):
    def get(self, request):
        return Response({"questions": quiz.QUESTIONS})


class QuizResultView(APIView):
    def post(self, request):
        answers = request.data.get("answers")
        if not isinstance(answers, list) or not 1 <= len(answers) <= len(quiz.QUESTIONS) or any(a not in quiz.MOODS for a in answers):
            return Response({"answers": ["Send 1 to 5 valid answers."]}, status=status.HTTP_400_BAD_REQUEST)
        mood = quiz.score(answers)
        qs = Package.objects.filter(is_published=True)
        matches = qs.filter(moods__icontains=mood)
        if mood == "family":
            matches = qs.filter(Q(moods__icontains="family") | Q(suits_kids=True) | Q(category="family"))
        picks = list(matches[:3]) or list(qs.filter(is_featured=True)[:3])
        return Response({
            "mood": {"key": mood, **quiz.MOODS[mood]},
            "packages": PackageListSerializer(picks, many=True, context={"request": request}).data,
        })


# ------------------------------------------------------------------ group trip room
def room_payload(room, request):
    options = []
    for o in room.options.select_related("package").prefetch_related("votes").order_by("id"):
        p = o.package
        voters = [v.voter_name for v in o.votes.all()]
        options.append({
            "id": o.id,
            "package": {
                "slug": p.slug, "title": p.title, "summary": p.summary, "duration_days": p.duration_days,
                "image": request.build_absolute_uri(p.image.url) if p.image else None,
            },
            "votes": len(voters), "voters": voters,
            "per_person": int(p.price_from), "total": int(p.price_from) * room.travellers,
        })
    people = sorted({v.voter_name for v in room.room_votes.all()})
    return {"code": room.code, "title": room.title, "travellers": room.travellers, "options": options, "people": people}


class RoomCreateView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "room_create"

    def post(self, request):
        title = str(request.data.get("title", "")).strip()[:80]
        slugs = request.data.get("package_slugs")
        try:
            travellers = int(request.data.get("travellers", 2))
        except (TypeError, ValueError):
            travellers = 0
        errors = {}
        if not title:
            errors["title"] = ["Give your trip a name."]
        if not 1 <= travellers <= 50:
            errors["travellers"] = ["Enter 1 to 50 travellers."]
        if not isinstance(slugs, list) or not all(isinstance(x, str) for x in slugs) or not 2 <= len(set(slugs)) <= 5:
            errors["package_slugs"] = ["Pick 2 to 5 packages."]
        ordered = list(dict.fromkeys(slugs)) if not errors.get("package_slugs") else []  # keep the order they were picked in
        by_slug = {p.slug: p for p in Package.objects.filter(slug__in=ordered, is_published=True)}
        if ordered and len(by_slug) != len(ordered):
            errors["package_slugs"] = ["One of those packages is not available."]
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        room = Room.objects.create(title=title, travellers=travellers)
        RoomOption.objects.bulk_create([RoomOption(room=room, package=by_slug[x]) for x in ordered])
        return Response({"code": room.code}, status=status.HTTP_201_CREATED)


class RoomDetailView(APIView):
    def get(self, request, code):
        try:
            room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(room_payload(room, request))


class RoomVoteView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "room_vote"

    def post(self, request, code):
        try:
            room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        name = str(request.data.get("voter_name", "")).strip()[:40]
        token = str(request.data.get("voter_token", ""))
        option = room.options.filter(pk=request.data.get("option_id") or 0).first()
        errors = {}
        if not name:
            errors["voter_name"] = ["Enter your name to vote."]
        if not 8 <= len(token) <= 64:
            errors["voter_token"] = ["Invalid voter token."]
        if option is None:
            errors["option_id"] = ["Pick one of the options."]
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        RoomVote.objects.update_or_create(room=room, voter_token=token, defaults={"option": option, "voter_name": name})
        return Response(room_payload(room, request))