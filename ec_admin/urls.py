from django.urls import path
from . import views

app_name = "ec_admin"

urlpatterns = [
    path('', views.admin, name="admin"),
    path('add_voter/', views.add_voter, name="add_voter"),
    path('add_candidate/', views.add_candidate, name="add_candidate"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('election_setup/', views.election_setup, name="election_setup"),
    path('election_setup/', views.election_setup, name="election_setup"),
    path('set_up/', views.set_up, name="set_up"),
    path('add_category/', views.add_category, name="add_category"),
    path('voter_register/', views.voter_register, name="voter_register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('start_election/', views.start_election, name="start_election"),
    path('edit_voter/<str:voter_id>/', views.edit_voter, name="edit_voter"),
    path('delete/<int:voter_id>/', views.delete, name="delete"),
    path('candidates/', views.candidates, name="candidates"),
    path('close_election/', views.close_election, name="close_election"),
    path('close_election/<int:election_id>/', views.close_election, name="close_election"),
    path('edit_candidate/<int:candidate_id>', views.edit_candidate, name="edit_candidate"),
    path('voter_register_to_pdf', views.voter_register_to_pdf, name="voter_register_to_pdf"),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name="delete_candidate"),
    path('result_pdf/', views.result_pdf, name="result_pdf"),
    path('results/', views.results, name="results"),
]