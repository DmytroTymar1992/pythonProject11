from django.contrib import admin
from .models import Resume, Education, WorkExperience, Course, Language, UserLanguage

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_created')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'education_level', 'start_date')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'proficiency_level')
