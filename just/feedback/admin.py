from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'job_seeker', 'resume')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'
