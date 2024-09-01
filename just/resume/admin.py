from django.contrib import admin
from .models import Resume, Education, WorkExperience, Course, Language, UserLanguage

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_created', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'education_level', 'start_date', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'proficiency_level', 'display_str')

    def display_str(self, obj):
        return str(obj)
    display_str.short_description = 'String Representation'
