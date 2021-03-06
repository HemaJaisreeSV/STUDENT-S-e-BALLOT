from django.urls import path
from . import views

urlpatterns = [
    path('', views.base),
    path('base', views.base,name='base'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('staff', views.staff,name='staff'),
    path('voter', views.voter,name='voter'),
    path('candidate', views.candidate,name='candidate'),
    path('chome', views.chome,name='chome'),
    path('shome', views.shome,name='shome'),
    path('vhome', views.vhome,name='vhome'),
    path('new_elections', views.new_elections,name='new_elections'),
    path('add_voters', views.add_voters,name='add_voters'),
    path('sview_elections', views.sview_elections,name='sview_elections'),
    path('vview_candidates', views.vview_candidates,name='vview_candidates'),
    path('sview_candidates', views.sview_candidates,name='sview_candidates'),
    path('sview_results', views.sview_results,name='sview_results'),
    path('vview_results', views.vview_results,name='vview_results'),
    path('vvoting', views.vvoting,name='vvoting'),
    path('SECRETARY', views.SECRETARY,name='SECRETARY'),
    path('ASSISTANTSECRETARY', views.ASSISTANTSECRETARY,name='ASSISTANTSECRETARY'),
    path('PRESIDENT', views.PRESIDENT,name='PRESIDENT'),
    path('VICEPRESIDENT', views.VICEPRESIDENT,name='VICEPRESIDENT'),
    path('eligibilitycheck/',views.eligibilitycheck, name='eligibilitycheck'),
    path('voterlogout/',views.voterlogout, name='voterlogout'),
    path('adminlogout/',views.adminlogout, name='adminlogout'),
    path('candidatelogout/',views.candidatelogout, name='candidatelogout'),
    path('addvote/',views.addvote, name='voting'),
    path('viewresult',views.viewresult, name='viewresult'),
    path('singleresult/',views.singleresult, name='singleresult'),
    path('finalresult',views.finalresult, name='finalresult'),
    path('finalresultvoter',views.finalresultvoter, name='finalresultvoter'),
    path('finalresultcandidate',views.finalresultcandidate, name='finalresultcandidate')
     ]
