from django.urls import path
from . import views


app_name = "Poll_app"
urlpatterns = [
    path('login/', views.login),
    path('polls/', views.get_polls),
    path('polls/create_poll/', views.create_poll),
    path('polls/update_poll/<int:poll_id>/', views.update_poll),
    path('questions/create_question/', views.create_question),
    path('questions/update_question/<int:question_id>/', views.update_question),
    path('choices/create_choice/', views.create_choice),
    path('choices/update_choice/<int:choice_id>/', views.update_choice),  
    path('answers/<int:user_id>/', views.get_answers),
    path('answers/create_answer/', views.create_answer),
]