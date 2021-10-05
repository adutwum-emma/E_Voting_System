from django.contrib import admin
from .models import Election, Category, Vote, Voter, Candidate, Current_Election

admin.site.register(Election)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Current_Election)