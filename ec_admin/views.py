from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from index.models import Category, Candidate, Current_Election, Election, Voter, Vote
from django.contrib.auth.models import User
from datetime import datetime, date
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from xhtml2pdf import pisa


def admin(request):

    try:
        request.session["member_id"]
        return redirect("ec_admin:dashboard")
    except KeyError:
        pass
    
    return redirect("ec_admin:login")

def dashboard(request):

    voter = Voter.objects.all()
    total_users = User.objects.all()
    election_count = Election.objects.all()
    count_voters = Voter.objects.filter(has_voted=True)
    
    global election_id
    current = Current_Election.objects.all()

    for id in current:
        election_id = id.election_id

    election = Election.objects.get(id=int(election_id))


    context = {
        'election':election,
        'voter':voter,
        'count_voters':count_voters,
        'election_count':election_count,
    }

    try:
        request.session["member_id"]
        return render(request, "ec_admin/dashboard.html", context)
    except KeyError:
        pass

    return redirect("ec_admin:login")

def add_voter(request):

    if request.method == "POST":

        username = request.POST["username"]
        first_name = request.POST["first_name"]
        middle_name = request.POST["middle_name"]
        last_name = request.POST["last_name"]
        gender = request.POST["gender"]
        email = request.POST["email"]
        dob = request.POST["dob"]

        context = {
            'username':username,
            'first_name':first_name,
            'last_name':last_name,
            'middle_name':middle_name,
            'email':email,
            'gender':gender,
            'dob':dob
        }
        
        if Voter.objects.filter(email=email).exists():

            messages.error(request, "Email already exists")
            return render(request, "ec_admin/add_voter.html", context)
        
        elif Voter.objects.filter(user_name=username).exists():

            messages.error(request, "Username already exists")
            return render(request, "ec_admin/add_voter.html", context)

        else:

            voter = Voter.objects.create(
                user_name=username,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                email=email
            )
            voter.save()

            messages.info(request, "Voter added successfully")
            return redirect("ec_admin:add_voter")

    else:

        try:

            request.session["member_id"]
            return render(request, "ec_admin/add_voter.html")

        except KeyError:
        
            pass

        return redirect("ec_admin:login")


def edit_voter(request, voter_id):

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        email = request.POST['email']  

        voter = Voter.objects.get(id=voter_id)
        voter.user_name=username
        voter.first_name=first_name
        voter.middle_name=middle_name
        voter.last_name=last_name
        voter.gender=gender
        voter.dob=dob
        voter.email=email
        voter.save()

        return HttpResponse("Changed successfully")

    else:
        

        try:
            request.session["member_id"]
            voter = Voter.objects.get(id=voter_id)
            todays_date = date.today()

            context = {
                'voter':voter,
                'date_today':todays_date
            }

            return render(request, "ec_admin/edit_voter.html", context)

        except KeyError:
            pass
        
        return redirect("ec_admin:login")

    

    

def add_candidate(request):

    global e_id
    current = Current_Election.objects.all()

    for e in current:
        e_id = e.election_id

    election = Election.objects.get(id=e_id)

    context = {
        'election':election,
    }

    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        middle_name = request.POST["middle_name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        picture = request.FILES["file"]
        category = request.POST["category"]

        cat = Category.objects.get(id=int(category))

        candidate = Candidate.objects.create(

            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            dob=dob,
            gender=gender,
            profile_pic=picture,
            category=cat

        )
        candidate.save()

        messages.info(request, "Candidate added successfully")
        return redirect("ec_admin:add_candidate")
        
    else:


        try:

            request.session["member_id"]
            return render(request, 'ec_admin/add_candidate.html', context)

        except KeyError:
            
            pass

        return redirect("ec_admin:login")

def election_setup(request):

    user = User.objects.get(id=int(request.session["member_id"]))

    context = {
        'user':user
    }

    try:
        request.session["member_id"]
        return render(request, 'ec_admin/election_setup.html', context)

    except KeyError:
        pass

    return redirect("ec_admin:login")

def set_up(request):

    try:
        
        election_name = request.POST["election"]
        date_start = request.POST["date_to_start"]
        date_end = request.POST["date_to_end"]
        ec_id = request.session["member_id"]

        user = User.objects.get(id=ec_id)

        election = Election.objects.create(
            election_name=election_name,
            electoral_commission=user,
            time_to_start=date_start,
            time_to_end=date_end
        )

        election.save()

        messages.info(request, "Election is set up successfully")

        return redirect("ec_admin:election_setup")

    except KeyError:
        return HttpResponse("Key error...you may need to login before")

def add_category(request):

    try:
        
        category_name = request.POST["category_name"]
        selected_election = request.POST["election"]

        election = Election.objects.get(id=int(selected_election))

        category = Category.objects.create(
            election=election,
            category_name=category_name
        )
        category.save()

        messages.info(request, "Category added successfully")
        return redirect("ec_admin:election_setup")

    except KeyError:
        return HttpResponse("Key Error... maybe you need to login first")


def start_election(request):

    try:
            
        request.session["member_id"]

        election = request.POST["election"]

        current = Current_Election.objects.all()
        current.delete()

        new_election = Election.objects.get(id=int(election))

        set_current = Current_Election.objects.create(
            election_id=new_election.id
        )
        set_current.save()

        set_electon = Election.objects.get(id=int(election))
        set_electon.has_started = True
        set_electon.real_time_started = datetime.today()
        set_electon.save()

        messages.info(request, "Election started successfully")
        return redirect("ec_admin:dashboard")

    except KeyError:
        pass
    return HttpResponse("<h4>Invalid action, maybe you need to login first</h4>")



def voter_register(request):

    voter = Voter.objects.all()

    try:
        request.session["member_id"]

        context = {
            'voter':voter,
        }

        return render(request, "ec_admin/voters.html", context)
        
    except KeyError:
        pass

    return redirect("ec_admin:login")

    
        
    

def login(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            request.session["member_id"] = user.id
            auth.login(request, user)
            return redirect("ec_admin:admin")
        else:
            messages.info(request, "Ivalid login")
            return render(request, "ec_admin/admin_login.html", {'username':username})

    else:
        return render(request, "ec_admin/admin_login.html")

def delete(request, voter_id):

    try:

        request.session["member_id"]
        voter = Voter.objects.get(id=voter_id)
        voter.delete()
        return HttpResponse("Deleted successfully")

    except KeyError:
        pass

    return redirect("ec_admin:login")

def logout(request):
    try:
        auth.logout(request)
        del request.session["member_id"]
    except KeyError:
        pass
    return redirect("ec_admin:login")


def candidates(request):

    try:
        request.session["member_id"]
        candidate = Candidate.objects.all()
        todays_date = date.today()

        context = {
            'candidate':candidate,
            'date':todays_date
        }

        return render(request, "ec_admin/candidate_list.html", context)

    except :
        pass
    
    return redirect("ec_admin:login")

def edit_candidate(request, candidate_id):

    if request.method == "POST":
        
        first_name = request.POST["first_name"]
        middle_name = request.POST["middle_name"]
        last_name = request.POST["last_name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        old_pic = request.POST['old_pic']
        category_id = request.POST["category"]

        try:
            pic = request.FILES["pic"]
            category = Category.objects.get(id=category_id)

            candidate = Candidate.objects.get(id=candidate_id)
            candidate.first_name=first_name
            candidate.middle_name=middle_name
            candidate.last_name=last_name
            candidate.gender=gender
            candidate.profile_pic=pic
            candidate.category=category
            candidate.save()
        except KeyError:
            
            category = Category.objects.get(id=category_id)

            candidate = Candidate.objects.get(id=candidate_id)
            candidate.first_name=first_name
            candidate.middle_name=middle_name
            candidate.last_name=last_name
            candidate.gender=gender
            candidate.profile_pic=old_pic
            candidate.category=category
            candidate.save()

        return HttpResponse("Updated successfully")

    else:


        try:
            request.session["member_id"]
            global e_id
            current = Current_Election.objects.all()
            todays_date = date.today()

            for e in current:
                e_id = e.election_id

            election = Election.objects.get(id=e_id)
            candidate = Candidate.objects.get(id=candidate_id)

            context = {
                'election':election,
                'candidate':candidate,
                'date':todays_date
            }

            return render(request, "ec_admin/edit_candidate.html", context)

        except KeyError:
            pass
        
        return redirect("ec_admin:login")

    


def close_election(request, election_id):

    try:
        request.session["member_id"]
        election = Election.objects.get(id=election_id)
        election.has_closed = True
        election.save()

        return redirect("ec_admin:dashboard")
    except KeyError:
        pass

    return HttpResponse("<h2>Error, maybe you need to log in</h2>")

def delete_candidate(request, candidate_id):

    try:
        request.session["member_id"]

        candidate = Candidate.objects.get(id=candidate_id)
        candidate.delete()

        return redirect("ec_admin:candidates")
    except print(0):
        pass

    return redirect("ec_admin:login")
    


def voter_register_to_pdf(request):
    
    voter = Voter.objects.all()
    my_date = date.today()

    template_path = 'ec_admin/voterregister.html'
    context = {
        'voter': voter,
        'my_date':my_date
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    #if you want to display in the browser get rid of the attatchment
    response['Content-Disposition'] = 'filename="voter_register.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def result_pdf(request):


    try:
        request.session["member_id"]
        global election_id
        current = Current_Election.objects.all()
        date_today = date.today

        for e in current:
            election_id = e.election_id

        election = Election.objects.get(id=election_id)

        template_path = 'ec_admin/results_pdf.html'
        my_date = date.today()
        context = {
            'election':election,
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')


        #if you want to display in the browser get rid of the attatchment
        response['Content-Disposition'] = 'filename="voter_register.pdf"'


        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        
    except KeyError:
        pass
    return redirect("ec_admin:login")
    

def results(request):

    try:
        request.session["member_id"]

        global election_id
        current = Current_Election.objects.all()
        date_today = date.today

        for e in current:
            election_id = e.election_id

        election = Election.objects.get(id=election_id)

        my_date = date.today()
        context = {
            'election':election,
        }

        return render(request, "ec_admin/results.html", context)

    except KeyError:
        pass
    
    return redirect("ec_admin:login")

