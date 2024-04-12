from django.db import models
from django.contrib.auth.models import User
import json

class PresentMeeting(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    onprogress = models.BooleanField(default=False)
    participants = models.TextField(default='[]')  # Store participants as JSON array

    def get_participants(self):
        return json.loads(self.participants)
    
    def add_participant(self, participant_id):
        participants = self.get_participants()
        if participant_id not in participants:
            participants.append(participant_id)
            self.participants = json.dumps(participants)
            self.save()