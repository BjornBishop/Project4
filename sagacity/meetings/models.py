from django.db import models

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, time
from jobs.models import JobPosting

class Meeting(models.Model):
    MEETING_TYPES = [
        ('initial', 'Initial Discussion'),
        ('processes', 'CV adjusting & Motivations'),
        ('Interview', 'Interview Preparation'),
    ]
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='meetings')
    candidate_name = models.CharField(max_length=100)
    candidate_email = models.EmailField()
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.time:
            meeting_time = self.time
            start_time = time(9, 0)  # 9:00
            end_time = time(17, 0)   # 17:00
            
            if meeting_time < start_time or meeting_time > end_time:
                raise ValidationError('Meetings must be scheduled between 9:00 and 17:00')
        
        # Check for existing meetings at the same time
        existing_meetings = Meeting.objects.filter(
            date=self.date,
            time=self.time
        ).exclude(pk=self.pk)
        
        if existing_meetings.exists():
            raise ValidationError('This time slot is already booked')
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['date', 'time']
    
    def __str__(self):
        return f"{self.candidate_name} - {self.job.title} - {self.date} {self.time}"