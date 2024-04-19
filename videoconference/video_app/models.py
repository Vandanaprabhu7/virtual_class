from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import json
from django.utils import timezone

class PresentMeeting(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    onprogress = models.BooleanField(default=False)
    participants = models.TextField(default="")
    join_times = models.JSONField(default=dict)
    leave_times = models.JSONField(default=dict)
    interval=models.JSONField(default=dict)
    secname = models.CharField(max_length=100, unique=True)
    def get_participants(self):
        if self.participants:
            return self.participants.split(',')  # Split the string by comma (or any other delimiter you choose)
        else:
            return []

    def add_participant(self, participant_id):
        participants = self.get_participants()
        join_time = timezone.now()  # Get current time
        if str(participant_id) not in participants:  # Convert participant_id to string for comparison
            participants.append(str(participant_id))
            self.participants = ','.join(participants)  # Join the list with comma as delimiter
            # Update join_times dictionary
            self.join_times[str(participant_id)] = join_time.strftime("%Y-%m-%d %H:%M:%S")
            self.save()

    def add_leave_time(self, participant_id):
        leave_time = timezone.now()
        join_time = datetime.strptime(self.join_times[str(participant_id)], "%Y-%m-%d %H:%M:%S")
        leave_time = datetime.strptime(leave_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        self.leave_times[str(participant_id)] = leave_time.strftime("%Y-%m-%d %H:%M:%S")
        time_difference = leave_time - join_time

        # Convert time difference to hours, minutes, seconds
        hours, remainder = divmod(time_difference.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        time_format = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        
        # Add interval to the previous one if it exists
        if self.interval.get(str(participant_id)):
            prev_interval = datetime.strptime(self.interval[str(participant_id)], "%H:%M:%S")
            new_interval = prev_interval + time_difference
            self.interval[str(participant_id)] = new_interval.strftime("%H:%M:%S")
        else:
            self.interval[str(participant_id)] = time_format
        
        self.save()
class sectionDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secname = models.CharField(max_length=100, unique=True)
    students=models.TextField(default="")
    
    def getusn(self,participant_id):
        student_usns = self.students.split(',')
        if 0 <= participant_id < len(student_usns):
            return student_usns[participant_id]
        else:
            return None
