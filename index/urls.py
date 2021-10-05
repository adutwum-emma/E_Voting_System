from django.urls import path
from . import views

app_name = "index"

urlpatterns = [
    path('', views.login, name="login"),
    path('voting/', views.voting, name="voting"),
    path('voter_logout/', views.voter_logout, name="voter_logout")
]
