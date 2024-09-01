from django.urls import path
from .views import *


urlpatterns = [
    path('vacancy/<int:vacancy_id>/feedback/', save_feedback, name='save_feedback'),
    path('employer/feedbacks/', employer_feedback_list, name='employer_feedback_list'),
    path('feedback/update-status/<int:feedback_id>/', update_feedback_status, name='update_feedback_status'),
    path('feedbacks/<int:vacancy_id>/', employer_feedback_list, name='employer_feedback_list_filtered'),
    path('feedback/vacancy/<int:vacancy_id>/lead_feedback/', save_lead_feedback, name='save_lead_feedback'),



]
