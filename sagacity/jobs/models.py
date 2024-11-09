from django.db import models

# Create your models here.
# jobs/models.py
from django.db import models
from django.urls import reverse

class JobPosting(models.Model):
    DURATION_CHOICES = [
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months'),
        ('Try-&-Hire', 'Try-&-Hire'),
    ]
    
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    max_rate = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    requirements = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-posted_date']
        
    def __str__(self):
        return f"{self.title} - {self.duration}"
    
    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} ({self.created_at})"