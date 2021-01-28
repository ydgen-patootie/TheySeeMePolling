from django.urls import path
from . import views


app_name = "Poll_app"
urlpatterns = [
    path('login/', views.login),
    path('polls/', views.get_polls),
    path('polls/create_poll/', views.create_poll),
]