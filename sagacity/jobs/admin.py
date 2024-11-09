from django.contrib import admin

# Register your models here.
# jobs/admin.py
from django.contrib import admin
from .models import JobPosting, Contact

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'max_rate', 'posted_date', 'is_active')
    list_filter = ('duration', 'is_active', 'posted_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'posted_date'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'created_at'

# meetings/admin.py
from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'job', 'meeting_type', 'date', 'time')
    list_filter = ('meeting_type', 'date')
    search_fields = ('candidate_name', 'candidate_email')
    date_hierarchy = 'date'