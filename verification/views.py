from django.shortcuts import render, redirect
from django.http import HttpResponse
from index.models import Voter
from random import *
from django.contrib import messages

def voter_verification(request):

    voter_pass = random_password()

    if request.method == "POST":
        voter_id = request.POST["voter_id"]

        if Voter.objects.filter(user_name=voter_id).exists():

            voter = Voter.objects.get(user_name=voter_id)

            if voter.isVerified:
                return HttpResponse('<span style="color:red;">Voter already verified</span>') 
            else:
                voter.password = voter_pass
                voter.isVerified = True
                voter.save()
                return HttpResponse('<span style="color: blue;">' + voter_pass + '</span>')
        else:
            return HttpResponse('<span style="color:red;">Voter ID does not exist</span>')
            
    else:
        
        return render(request, "verification/verification.html")

def random_password():
    limit = 5
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    generated = []

    for e in range(limit):
        generated.append(choice(text))
    
    result = "".join(generated)

    return result

