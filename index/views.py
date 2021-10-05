from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Voter
from django.contrib import messages
from .models import Current_Election, Category, Election, Candidate, Vote, Voter


def login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        context = {
            'username': username,
        }

        voter = Voter.objects.filter(
            user_name=username,
            password=password
        )

        if voter.exists():

            get_voter = Voter.objects.get(user_name=username)

            if not get_voter.has_voted:
    
                request.session['member_id'] = get_voter.id
                return redirect('index:voting')
            else:
                messages.info(request, "You have already voted")
                return redirect("/")
        else:
            messages.error(request, "Invalid login")
            return render(request, "index/voter_login.html", context)
    else:
        return render(request, "index/voter_login.html")


def voter_logout(request):

    try:
        del request.session['member_id']
    except KeyError:
        pass

    return redirect("/")


def voting(request):

    global election_id
    current = Current_Election.objects.all()
    

    for id in current:
        election_id = id.election_id

    election = Election.objects.get(id=election_id)
    category = Category.objects.filter(election_id=election.id)

    context = {
        'election': election
    }
    

    if request.method == "POST":
    
        for data in category:
            e_id = request.POST[str(data.id)]
            cat = Category.objects.get(id=int(data.id))
            candidate = Candidate.objects.get(id=e_id)
            vote = Vote.objects.create(
                candidate=candidate,
                election=election,
                category=cat
            )
            vote.save()
        
        voter = Voter.objects.get(id=int(request.session["member_id"]))
        voter.has_voted = True
        voter.save()
        
        messages.info(request, "You have voted successfully")
        return redirect("index:voter_logout")
            

    else:

        try:
            request.session["member_id"]
            return render(request, "index/voting_interface.html", context)
        except KeyError:
            pass
        return redirect("/")
    