import secrets

from django.db import models

from packages.models import Package


class Room(models.Model):
    code = models.CharField(max_length=12, unique=True, editable=False)
    title = models.CharField(max_length=80)
    travellers = models.PositiveSmallIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        while not self.code:
            candidate = secrets.token_urlsafe(6).lower().replace("_", "x").replace("-", "y")
            if not Room.objects.filter(code=candidate).exists():
                self.code = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.code})"


class RoomOption(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="options")
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room.code}: {self.package.title}"


class RoomVote(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_votes")
    option = models.ForeignKey(RoomOption, on_delete=models.CASCADE, related_name="votes")
    voter_name = models.CharField(max_length=40)
    voter_token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["room", "voter_token"], name="one_vote_per_person_per_room")]