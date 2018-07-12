# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from datetime import date
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.shortcuts import render, render_to_response, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
import forms
from .forms import UserForm, StudentForm, CandidateForm, DepartmentForm, PostForm, ElectionForm
from django.contrib.auth.models import User
from .models import Department, Election, Student, Candidate, Post, FacultyElection, DepartmentElection, Exco

# Create your views here.

def index(request):
	#context = RequestContext(request)
	template = loader.get_template('elections/index.html')
	return HttpResponse(template.render({}, request))
    

def signup(request):
	context = RequestContext(request)
	registered = False
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		student_form = StudentForm(data=request.POST)
		#profile_form = UserProfileForm(data=request.POST)
		# If the two forms are valid...
		

		if user_form.is_valid() and student_form.is_valid():
			# Save the user's form data to the database.

			user = user_form.save(commit=False)
			user.is_active = False
			user.set_password(user.password)
			user.save()

			student = student_form.save(commit=False)
			#profile.user = user

			if 'picture' in request.FILES:
				student.picture = request.FILES['picture']

				student.save()
				registered = True
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('elections/acc_active_email.html', {'user': user,'domain': current_site.domain, 'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':account_activation_token.make_token(user),})
			to_email = user_form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			
		else:
			print user_form.errors, student_form.errors
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
		
		
	else:
		user_form = UserForm()
		student_form = StudentForm()
		# Render the template depending on the context.
	return render(request, 'elections/signup.html', {'user_form': user_form, 'student_form':student_form, 'registered': registered})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def authLogin(request):
	context = RequestContext(request)
	if request.method == 'POST':
	    #Gather the username and password provided by the user.
        # This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		
		# Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.

		user = authenticate(username=username, password=password)

		if user is not None:
			# Is the account active? It could have been disabled.
			if user.is_active:
				#try:
				login(request, user)
				if user.is_staff:
					user_form = UserForm()
					post_form = PostForm()
					department_form = DepartmentForm()
					election_form = ElectionForm()
					# Render the template depending on the context.
					return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form':post_form, 'department_form': department_form, 'election_form': election_form})

				else:	
					std = Student.objects.get(matricule=username)
					candidate_form = CandidateForm()
					dept = std.department.name
					election = Election.objects.filter(year=2018, department=std.department).first() 
					dte = election.duedate
					currentdate = date.today()
					message = False
					if currentdate > dte:
						message = True
						if std.status:
							return render(request, 'elections/candate.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
						else:
							return render(request, 'elections/student.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
					else:
						message = False
						if std.status:
							return render(request, 'elections/candate.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
						else:
							return render(request, 'elections/student.html', {'std': std, 'candidate_form': candidate_form, 'message': message})


					"""except (RuntimeError, TypeError, NameError):
					errmessage = (RuntimeError, TypeError, NameError)
					CapturLog().logdata(request, 'LoginError', 'Login', errmessage)"""
		
			else:
				return HttpResponse("Your account is disabled")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")

	else:
		return render(request, 'elections/login.html', {})
"""function that returns the student dashboard view """
def studentDashboard(request):
	if request.user.is_authenticated():
		username = request.user.username
		std = Student.objects.get(matricule=username)
		candidate_form = CandidateForm()
		dept = std.department.name
		election = Election.objects.filter(year=2018, department=std.department).first() 
		dte = election.duedate
		currentdate = date.today()
		message = False
		if currentdate > dte:
			message = True
			if std.status:
				return render(request, 'elections/candate.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
			else:
				return render(request, 'elections/student.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
		else:
			message = False
			if std.status:
				return render(request, 'elections/candate.html', {'std': std, 'candidate_form': candidate_form, 'message': message})
			else:
				return render(request, 'elections/student.html', {'std': std, 'candidate_form': candidate_form, 'message': message})

"""logout function"""
def authLogout(request):
	logout(request)
	return render(request, 'elections/index.html', {})

def profile(request):
	context = RequestContext(request)
	message = False
	usrname = request.user.username

	if request.method == 'GET':
		std = Student.objects.get(matricule=usrname)

	else:
		username = request.POST['username']
		password = request.POST['password']
		newpassword = request.POST['newpassword']
		confirmpassword = request.POST['confirmpassword']

	"""	if request.user.is_authenticated():
			encoded = request.user.password

			student = Student.objects.get(matricule=request.user.usrname)
			if check_password(password, encoded) and newpassword == confirmpassword:
				password = make_password(confirmpassword, salt=None, hasher=’default’)
				user.password = password
				user.save()
				message = True"""
	
	
	return render(request, 'elections/profile.html', {'message':message, 'std':std})


def candidateApplication(request):
	context = RequestContext(request)
	std = Student.objects.get(matricule=request.user.username)
	message = False
	if request.method == 'POST':
		if request.user.is_authenticated():
				candidate_form = CandidateForm(data=request.POST)
				#profile_form = UserProfileForm(data=request.POST)

				if candidate_form.is_valid():
					candidate = candidate_form.save(commit=False)
					candidate.student = std
					candidate.department = std.department
					candidate.save()
					message = True

				else:
					print candidate_form.errors

	else:
		candidate_form = CandidateForm()

	return render(request, 'elections/student.html', {'std': std, 'candidate_form': candidate_form, 'message':message})

def detail(request, candidate_id):
	context = RequestContext(request)
	std = Student.objects.get(matricule=request.user.username)
	if request.method == 'GET':
		candidate = Candidate.objects.get(pk=candidate_id)

		return render(request, 'elections/individual.html', {'std': std, 'candidate': candidate})



def vote(request, candidate_id):
	if request.user.is_authenticated():
		candidate = Candidate.objects.get(pk=candidate_id)
		votes = candidate.votes
		std = Student.objects.get(matricule=request.user.username)
		dept = Department.objects.get(name=std.department.name)
		posit = Post.objects.get(pk=candidate.post.id)
		#exists() could be used instead of first. It returns true or false
		election = DepartmentElection.objects.filter(student=std, post__id=posit.id).first()
		if election:
			message = 'You already voted'

		else:
			candidate.votes = votes + 1
			candidate.save()
			voter = DepartmentElection(post = posit, student = std, department = dept )
			voter.save()
			message = 'Your vote was successfully taken'

		return render(request, 'elections/vote.html', {'std':std, 'message':message})


#Returns departmental candidates
def departmentCandidate(request):
	#if user is logged in
	if request.user.is_authenticated():
		mat = request.user.username
		std = Student.objects.get(matricule=mat)
		dept = std.department.name
		candidates = Candidate.objects.filter(department__name=dept, status=True).order_by('post__name')
        return render(request, 'elections/candidate.html', {'candidates':candidates})


def result(request):
	context = RequestContext(request)
	if request.method == 'GET':
		if request.user.is_authenticated():
			mat = request.user.username
			std = Student.objects.get(matricule=mat)
			dept = std.department.name
			election = Election.objects.filter(year=2018, department=std.department).first() 
			dte = election.duedate
			currentdate = date.today()
			message = False
			if currentdate > dte :
				message = True
				candidates = Candidate.objects.filter(department__name=dept, status=True)
				e = DepartmentElection.objects.filter(department__name=dept)

				for candidate in candidates:
					q = e.filter(post=candidate.post)
					w = q.count()
					total = (candidate.votes/w)*100
					candidate.votes = total

				return render(request, 'elections/result.html', {'std': std, 'candidates': candidates, 'message': message})

			else:
				return render(request, 'elections/result.html', {'std': std, 'message': message})




#edits the candidate's campaign information
def editCampaign(request):
	context = RequestContext(request)
	if request.method == 'POST':
	    #Gather the information from the form supplied by the user
		mat = request.POST['username']
		whyapply = request.POST['whyapply']
		whyvote = request.POST['whyvote']

		if request.user.is_authenticated():
			std = Student.objects.get(matricule=mat)
			candidate = Candidate.objects.get(student=std)
			candidate.why_apply = whyapply
			candidate.why_vote = whyvote
			candidate.save()
			message = 'Campaign successfully modified'

		return render(request, 'elections/candate.html', {'std': std, 'message': message})

#adds a new adminstrator
def newAdmin(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		
		if user_form.is_valid():
			# Save the user's form data to the database.

			user = user_form.save(commit=False)
			user.is_staff = True
			user.set_password(user.password)
			user.save()
			message = 'New admin successfully added'
		else:
			print user_form.errors
		message = 'New admin was not successfully added'
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		
		
		
	else:
		user_form = UserForm()
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		message = 'New admin was not successfully added'
		# Render the template depending on the context.
	return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form': post_form, 'department_form': department_form, 'election_form': election_form, 'message': message})

def loginAdmin(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			user_form = UserForm()
			post_form = PostForm()
			department_form = DepartmentForm()
			election_form = ElectionForm()
		# Render the template depending on the context.
			return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form':post_form, 'department_form': department_form, 'election_form': election_form})

		else:
			return render(request, 'elections/nopermission', {})

def allPost(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			posts = Post.objects.all()
		# Render the template depending on the context.
			return render(request, 'elections/post.html', {'posts': posts} )

		else:
			return render(request, 'elections/nopermission', {})

def allUser(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			users = User.objects.filter(is_active=True)
		# Render the template depending on the context.
			return render(request, 'elections/user.html', {'users': users} )

		else:
			return render(request, 'elections/nopermission.html', {})

def smeCandidate(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			candidates = Candidate.objects.exclude(status=1)
		# Render the template depending on the context.
			return render(request, 'elections/admincandidate.html', {'candidates': candidates} )

		else:
			return render(request, 'elections/nopermission.html', {})

def candidate(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			candidates = Candidate.objects.filter(status=1)
		# Render the template depending on the context.
			return render(request, 'elections/adminallcandidate.html', {'candidates': candidates} )

		else:
			return render(request, 'elections/nopermission.html', {})






#adds new post
def newPost(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'POST':
		post_form = PostForm(data=request.POST)
		
		if post_form.is_valid():
			# Save the user's form data to the database.

			post = post_form.save()
			message = 'New post successfully added'
		else:
			print post_form.errors
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
			message = 'New post was not successfully added'
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		user_form = UserForm()
		
		
	else:
		user_form = UserForm()
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
	
		# Render the template depending on the context.
	return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form':post_form, 'department_form': department_form, 'election_form': election_form, 'message': message})





#adds new department
def newDepartment(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'POST':
		department_form = DepartmentForm(data=request.POST)
		
		if department_form.is_valid():
			# Save the user's form data to the database.

			department = department_form.save()
			message = 'New department successfully added'
			
		else:
			print department_form.errors
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
			message = 'New department was not successfully added'
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		user_form = UserForm()
		
		
		
	else:
		user_form = UserForm()
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		# Render the template depending on the context.
	return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form':post_form, 'department_form': department_form, 'election_form': election_form, 'message': message})







#adds new election
def newElection(request):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'POST':
		election_form = ElectionForm(data=request.POST)
		
		if election_form.is_valid():
			# Save the user's form data to the database.

			election = election_form.save()
			message = 'New election successfully added'
			
		else:
			print election_form.errors
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
			message = 'New election was not successfully added'
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		
		
	else:
		user_form = UserForm()
		post_form = PostForm()
		department_form = DepartmentForm()
		election_form = ElectionForm()
		# Render the template depending on the context.
	return render(request, 'elections/admin.html', {'user_form': user_form, 'post_form':post_form, 'department_form': department_form, 'election_form': election_form, 'message': message})


def deleteUser(request, user_id):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			user = User.objects.get(pk=user_id)
			user.is_active = False
			user.save()
			users = User.objects.filter(is_active=True)
			# Render the template depending on the context.
			return render(request, 'elections/user.html', {'users': users} )
			

		else:
			return render(request, 'elections/nopermission.html', {})

def acceptCandidate(request, candidate_id):
	context = RequestContext(request)
	# Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.

	if request.method == 'GET':
		if request.user.is_authenticated and request.user.is_staff:
			candidate = Candidate.objects.get(pk=candidate_id)
			candidate.status = 1
			candidate.save()
			candidates = Candidate.objects.exclude(status=1)
			# Render the template depending on the context.
			return render(request, 'elections/admincandidate.html', {'candidates': candidates} )
		else:
			return render(request, 'elections/nopermission.html', {})








		
		
