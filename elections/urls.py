from django.conf.urls import url
from views import *
from django.contrib import admin
from forms import * 
from django.contrib.auth import views as auth_views


urlpatterns = [
	
	url(r'^$', index, name='index'),
	url(r'^register/', signup, name='register'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
	url(r'^login/', authLogin, name='login'),
    url(r'^logout/$', authLogout, name='logout'),
    url(r'^student/$', studentDashboard, name='home'),
	url(r'^profile/$', profile, name='profile'),
	url(r'^application/$', candidateApplication, name='application'),
	url(r'^department/', departmentCandidate, name='department'),
	url(r'^post/', allPost, name='post'),
	url(r'^user/', allUser, name='user'),
	url(r'^deleteuser/(?P<user_id>\d+)/', deleteUser, name='deleteuser'),
	url(r'^campaign/', editCampaign, name='campaign'),
	url(r'^allcandidates/', candidate, name='candidates'),
	url(r'^admin/', loginAdmin, name='admin'),
	url(r'^addAdmin/', newAdmin, name='addAdmin'),
	url(r'^addDepartment/', newDepartment, name='addDepartment'),
	url(r'^addPost/', newPost, name='addPost'),
	url(r'^addElection/', newElection, name='addElection'),
	url(r'^futureCandidate/', smeCandidate, name='futureCandidate'),
	url(r'^result/', result, name='result'),
	url(r'^detail/(?P<candidate_id>\d+)/', detail, name='candidateinfo'),
	url(r'^acceptcandidacy/(?P<candidate_id>\d+)/', acceptCandidate, name='acceptcandidate'),
	url(r'^departmentelections/(?P<candidate_id>\d+)/', vote, name='departmentelections'),
	#url(r'^faculty/', facultyCandidate, name='facultycandidate')

]