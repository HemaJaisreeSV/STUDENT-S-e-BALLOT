from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.models import WinnerList,VotedLists, Admin, Candidate, Voter, Election , AcceptedCandidates
import mysql.connector
from operator import itemgetter
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

def base(request):
    return render(request,'Login/base.html')

def login(request):
    if request.method == "POST":
        login_as = request.POST['login_as']
        email = request.POST['email']
        password = request.POST['password']

        if login_as == 'ADMIN':
            admin_details = Admin.objects.filter(username=email,password=password).values_list('id')
            value = [i for j in admin_details for i in j ]         #first
            if value:
                res1 = Admin.objects.get(id=value[0])
                if res1.username == email and res1.password == password:
                    request.session['admin']=res1.id
                    res1 = Admin.objects.filter(id=value[0])
                    return render(request,'Login/shome.html',{'staff':res1})
            else:
                messages.info(request,"ADMIN'S USERNAME AND PASSWORD DOES NOT MATCH")
                return redirect('login')

        elif login_as == 'VOTER':
            try:
                res2= Voter.objects.get(Vemail_id__iexact = email)
                if res2.Vemail_id == email and res2.Vpassword == password:
                    request.session['voter'] = res2.VRegistration_Id
                    voter_details = Voter.objects.filter(Vemail_id__iexact = email)
                    return render(request,'Login/vhome.html',{'voter':voter_details})
            except ObjectDoesNotExist:
                messages.info(request,"VOTER'S USERNAME AND PASSWORD DOES NOT MATCH")
                return redirect('login')

        elif login_as == 'CANDIDATE':
            try:
                res3 = Candidate.objects.get(Cemail_id__iexact = email)
                if res3.Cemail_id == email and res3.Cpassword == password:
                    request.session['candidate'] = res3.CRegistration_Id
                    candidate_details = Candidate.objects.filter(Cemail_id__iexact = email)
                    return render(request,'Login/chome.html',{'candidate':candidate_details})
            except ObjectDoesNotExist:
                messages.info(request,"CANDIDATE'S USERNAME AND PASSWORD DOES NOT MATCH")
                return redirect('login')
        else:
            messages.info(request,'CHECK USERNAME AND PASSWORD')
            return redirect('login')
    return render(request,'Login/login.html')

def register(request):
    if request.method == "POST":
        candidate = Candidate()

        candidate.CRegistration_Id = request.POST['reg_id']
        candidate.Cname = request.POST['name']
        candidate.Cgender = request.POST['gender']
        candidate.Cdept = request.POST['dept']
        candidate.Cyear = request.POST['year']
        candidate.Cusername = request.POST['username']
        candidate.Cpassword = request.POST['password']
        candidate.Cmobile_no = request.POST['mob_no']
        candidate.Cemail_id = request.POST['email']
        candidate.Cposition = request.POST['position']

        if (candidate.CRegistration_Id == "" or candidate.Cname == "" or candidate.Cgender == "select" or candidate.Cdept == 'select'
            or candidate.Cyear == "select" or candidate.Cusername == "" or  candidate.Cpassword == ""
            or candidate.Cmobile_no == "" or candidate.Cemail_id == "" or candidate.Cposition == "") :
            messages.info(request,'SOME FIELDS ARE EMPTY')
            return redirect('register')
        elif Candidate.objects.filter(CRegistration_Id = candidate.CRegistration_Id).exists():
            messages.info(request,'REGISTRATION ID ALREADY EXISTS')
            return redirect('register')
        elif Candidate.objects.filter(Cusername = candidate.Cusername).exists():
            messages.info(request,'USERNAME ALREADY EXISTS')
            return redirect('register')
        elif Candidate.objects.filter(Cemail_id = candidate.Cemail_id).exists():
            messages.info(request,'MAIL-ID ALREADY EXISTS')
            return redirect('register')
        else:
            candidate.save()
            messages.info(request,'REGISTERED SUCCESSFULLY')
            return redirect('register')
    return render(request,'Login/register.html')

def staff(request):
    if request.session.has_key('admin'):
        admin_id = request.session['admin']
        admin_details = Admin.objects.filter(id = admin_id)
        return render(request,'Login/shome.html',{'admin':admin_details})
    else:
         return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO ADMIN ACCOUNT'})

def shome(request):
    if request.session.has_key('admin'):
        admin_id = request.session['admin']
        staff = Admin.objects.filter(id=admin_id)
        return render(request,'Login/shome.html',{'staff':staff})
    else:
        return redirect('login')

def new_elections(request):
    if request.session.has_key('admin'):
        admin_id = request.session['admin']
        if request.method == "POST":
            election = Election()

            election.e_Id = request.POST['eid']
            election.e_position = request.POST['eposition']
            election.e_title = request.POST['etitle']
            election.e_date = request.POST['edate']
            res1 = Admin.objects.get(id = admin_id)
            election.admin_id = res1.id

            if (election.e_Id  == "" or election.e_position == "select" or election.e_title == ""
                or  election.e_date == "") :
                messages.info(request,'SOME FIELDS ARE EMPTY')
                return redirect('new_elections')

            else:
                try:
                    elect = Election.objects.all()
                    if not elect :
                        election.save()
                        return render(request,'Login/new_elections.html')
                    for i in elect:
                        if election.e_position == i.e_position :
                            messages.info(request,"DUPLICATE ENTRIES FOR POSITION")
                            return render(request,'Login/new_elections.html')
                    election.save()
                except ObjectDoesNotExist:
                    election.save()
                    return render(request,'Login/new_elections.html')
        return render(request,'Login/new_elections.html')
    else:
        return redirect('login')

def add_voters(request):
    if request.session.has_key('admin'):
        admin_id = request.session['admin']
        if request.method == "POST":
            addvoter = Voter()
            addvoter.VRegistration_Id = request.POST['reg_id']
            addvoter.Vname = request.POST['name']
            addvoter.Vgender = request.POST['gender']
            addvoter.Vdept = request.POST['dept']
            addvoter.Vyear = request.POST['year']
            addvoter.Vusername = request.POST['username']
            addvoter.Vpassword = request.POST['password']
            addvoter.Vmobile_no = request.POST['mob_no']
            addvoter.Vemail_id = request.POST['email']
            res1 = Admin.objects.get(id=admin_id)
            addvoter.admin_id = res1.id

            if (addvoter.VRegistration_Id == "" or addvoter.Vname == "" or addvoter.Vgender == "select" or addvoter.Vdept == 'select'
                or addvoter.Vyear == "select" or addvoter.Vusername == "" or addvoter.Vpassword == ""
                or addvoter.Vmobile_no == "" or addvoter.Vemail_id == "" ) :
                messages.info(request,'SOME FIELDS ARE EMPTY')
                return redirect('add_voters')
            else:
                addvoter.save()
        return render(request,'Login/add_voters.html')
    else:
        return redirect('login')

def sview_elections(request):
    if request.session.has_key('admin'):
        v_elect = Election.objects.all()
        return render(request,'Login/sview_elections.html',{'v_elect':v_elect})
    else:
        return redirect('login')

def sview_results(request):
    if request.session.has_key('admin'):
        return render(request,'Login/sview_results.html')
    else:
        return redirect('login')

def sview_candidates(request):
    if request.session.has_key('admin'):
        sv_candid = Candidate.objects.all().exclude(status='accepted')
        accepted_list = AcceptedCandidates.objects.all()
        return render(request,'Login/sview_candidates.html',{'sv_candid':sv_candid,'accepted_list':accepted_list})
    else:
        return redirect('login')

def eligibilitycheck(request):
    if request.session.has_key('admin'):
        admin_id = request.session['admin']
    reject_id = request.GET.get('reject')
    accept_id = request.GET.get('accept')
    total_candidates = Candidate.objects.all().exclude(status='accepted')
    accepted_list = AcceptedCandidates.objects.all()                        #2
    if accept_id:
        candidate_details = Candidate.objects.get(CRegistration_Id=accept_id)
        check = AcceptedCandidates.objects.filter(candidate=candidate_details)
        if not check:
            candidate_details.status = 'accepted'
            res1 = Admin.objects.get(id=admin_id)
            candidate_details.admin_id = res1.id
            candidate_details.save()
            AcceptedCandidates.objects.create(candidate=candidate_details)
            return redirect('sview_candidates')

    if reject_id:
        Candidate.objects.filter(CRegistration_Id=reject_id).delete()
        return redirect('sview_candidates')

def vhome(request):
    if request.session.has_key('voter'):
        voter_id = request.session['voter']
        voter_details = Voter.objects.filter(VRegistration_Id = voter_id)
        return render(request,'Login/vhome.html',{'voter':voter_details})
    else:
        return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO VOTER ACCOUNT'})

def chome(request):
    if request.session.has_key('candidate'):
       # voter = Voter.objects.values(id__iexact = email)
        #res1 = Voter.objects.get(Vemail_id__iexact = email)   {'res1':res1}
        candidate_id = request.session['candidate']
        candidate_details = Candidate.objects.filter(CRegistration_Id = candidate_id)
        return render(request,'Login/chome.html',{'candidate':candidate_details})
    else:
        return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO CANDIDATE ACCOUNT'})


def vview_candidates(request):
    if request.session.has_key('voter'):
        vv_candid = Candidate.objects.filter(status='accepted')
        return render(request,'Login/vview_candidates.html',{'vv_candid':vv_candid})
    else:
        return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO VOTER ACCOUNT'})

def vvoting(request):
    if request.session.has_key('voter'):
        vote= Candidate.objects.all()
        elect = Election.objects.values('e_position')
        context = {'vote':vote,'elect':elect}
        return render(request,'Login/vvoting.html',context)
    else:
        return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO VOTER ACCOUNT'})

def addvote(request):
    candidate_id = request.GET.get('id')
    voter_id = request.session['voter']
    candidate_details = Candidate.objects.get(CRegistration_Id=candidate_id)
    voter_details = Voter.objects.get(VRegistration_Id=voter_id)
    check = VotedLists.objects.filter(votedcandidate=candidate_details,voter=voter_details)
    if not check:
        VotedLists.objects.create(votedcandidate=candidate_details,voter=voter_details)
        return redirect('/voter')

def SECRETARY(request):
    if request.session.has_key('voter'):
        voterid = request.session['voter']
        votingcheck = VotedLists.objects.filter(voter__VRegistration_Id=voterid)
        s = Candidate.objects.filter(Cposition='SECRETARY',status='accepted')
        return render(request,'Login/vote.html',{'s':s,'voted':votingcheck})
    else:
        return redirect('login')

def ASSISTANTSECRETARY(request):
    if request.session.has_key('voter'):
        voterid = request.session['voter']
        votingcheck = VotedLists.objects.filter(voter__VRegistration_Id=voterid)
        s = Candidate.objects.filter(Cposition='ASSISTANT SECRETARY',status='accepted')
        return render(request,'Login/vote.html',{'s':s,'voted':votingcheck})
    else:
        return redirect('login')

def PRESIDENT(request):
    if request.session.has_key('voter'):
        voterid = request.session['voter']
        votingcheck = VotedLists.objects.filter(voter__VRegistration_Id=voterid)
        s = Candidate.objects.filter(Cposition='PRESIDENT',status='accepted')
        return render(request,'Login/vote.html',{'s':s,'voted':votingcheck})
    else:
        return redirect('login')

def VICEPRESIDENT(request):
    if request.session.has_key('voter'):
        voterid = request.session['voter']
        votingcheck = VotedLists.objects.filter(voter__VRegistration_Id=voterid)
        s = Candidate.objects.filter(Cposition='VICE PRESIDENT',status='accepted')
        return render(request,'Login/vote.html',{'s':s,'voted':votingcheck})
    else:
        return redirect('login')

def vview_results(request):
    if request.session.has_key('voter'):
        return render(request,'Login/vview_results.html')
    else:
        return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO VOTER ACCOUNT'})

def voter(request):
    if request.session.has_key('voter'):
        voter_id = request.session['voter']
        voter_details = Voter.objects.filter(VRegistration_Id = voter_id)
        return render(request,'Login/vhome.html',{'voter':voter_details})
    else:
         return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO VOTER ACCOUNT'})

def candidate(request):
    if request.session.has_key('candidate'):
        candidate_id = request.session['candidate']
        candidate_details = Candidate.objects.filter(CRegistration_Id = candidate_id)
        return render(request,'Login/chome.html',{'candidate':candidate_details})
    else:
         return render(request,'Login/login.html',{'msg':'PLEASE LOGIN TO CANDIDATE ACCOUNT'})

def voterlogout(request):
    del request.session['voter']
    return redirect('/login')

def adminlogout(request):
    del request.session['admin']
    return redirect('login')

def candidatelogout(request):
    del request.session['candidate']
    return redirect('login')

def viewresult(request):
    return render(request,'login/adminviewresult.html')

def resultcalculation():
    items = ['SECRETARY','ASSISTANT SECRETARY','PRESIDENT','VICE PRESIDENT']
    for key in items:
        value = VotedLists.objects.filter(votedcandidate__Cposition=key).values_list('votedcandidate__CRegistration_Id')
        query = [i for j in value for i in j]
        query = list(dict.fromkeys(query))
        check = WinnerList.objects.filter(candidates__Cposition=key)
        if check:
            WinnerList.objects.filter(candidates__Cposition=key).delete()
        for i in query:
            details = Candidate.objects.get(CRegistration_Id=i)
            totalvote = VotedLists.objects.filter(votedcandidate__CRegistration_Id=i).count()
            WinnerList.objects.create(candidates=details,totalvote=totalvote)

def singleresult(request):
    if request.session.has_key('admin'):
        key = request.GET.get('key')
        value = VotedLists.objects.filter(votedcandidate__Cposition=key).values_list('votedcandidate__CRegistration_Id')
        query = [i for j in value for i in j]
        query = list(dict.fromkeys(query))
        check = WinnerList.objects.filter(candidates__Cposition=key)
        if check:
            WinnerList.objects.filter(candidates__Cposition=key).delete()
        for i in query:
            details = Candidate.objects.get(CRegistration_Id=i)
            totalvote = VotedLists.objects.filter(votedcandidate__CRegistration_Id=i).count()
            WinnerList.objects.create(candidates=details,totalvote=totalvote)
        result = WinnerList.objects.filter(candidates__Cposition=key)
        return render(request,'login/candidateresult.html',{'result':result})
    else:
        return redirect('login')

def finalresult(request):
    resultcalculation()
    if request.session.has_key('admin'):
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY')
        assistant = assistant.aggregate(Max('totalvote'))
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY',totalvote=assistant['totalvote__max'])

        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY')
        secretary = secretary.aggregate(Max('totalvote'))
        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY',totalvote=secretary['totalvote__max'])

        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT')
        president = president.aggregate(Max('totalvote'))
        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT',totalvote=president['totalvote__max'])

        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT')
        vicepresident = vicepresident.aggregate(Max('totalvote'))
        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT',totalvote=vicepresident['totalvote__max'])

        return render(request, 'login/finalresult.html', {'s':secretary,'a':assistant,'p':president,'v':vicepresident})
    else:
        return redirect('login')


def finalresultvoter(request):
    resultcalculation()
    if request.session.has_key('voter'):
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY')
        assistant = assistant.aggregate(Max('totalvote'))
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY',totalvote=assistant['totalvote__max'])

        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY')
        secretary = secretary.aggregate(Max('totalvote'))
        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY',totalvote=secretary['totalvote__max'])

        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT')
        president = president.aggregate(Max('totalvote'))
        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT',totalvote=president['totalvote__max'])

        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT')
        vicepresident = vicepresident.aggregate(Max('totalvote'))
        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT',totalvote=vicepresident['totalvote__max'])

        return render(request, 'login/finalresultvoter.html', {'s':secretary,'a':assistant,'p':president,'v':vicepresident})
    else:
        return redirect('login')

def finalresultcandidate(request):
    resultcalculation()
    if request.session.has_key('candidate'):
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY')
        assistant = assistant.aggregate(Max('totalvote'))
        assistant = WinnerList.objects.filter(candidates__Cposition='ASSISTANT SECRETARY',totalvote=assistant['totalvote__max'])

        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY')
        secretary = secretary.aggregate(Max('totalvote'))
        secretary = WinnerList.objects.filter(candidates__Cposition='SECRETARY',totalvote=secretary['totalvote__max'])

        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT')
        president = president.aggregate(Max('totalvote'))
        president = WinnerList.objects.filter(candidates__Cposition='PRESIDENT',totalvote=president['totalvote__max'])

        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT')
        vicepresident = vicepresident.aggregate(Max('totalvote'))
        vicepresident = WinnerList.objects.filter(candidates__Cposition='VICE PRESIDENT',totalvote=vicepresident['totalvote__max'])

        return render(request, 'login/finalresultcandidate.html', {'s':secretary,'a':assistant,'p':president,'v':vicepresident})
    else:
        return redirect('login')