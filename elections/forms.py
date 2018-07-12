from .models import Student, Candidate, Department, Post, Election
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

	email = forms.EmailField(max_length=200, help_text='Required')

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class  StudentForm(forms.ModelForm):

	class Meta:
		model = Student
		fields = ('firstname', 'lastname', 'department', 'matricule' , 'picture', 'dateofbirth', 'fathername', 'mothername')
	

		
class CandidateForm(forms.ModelForm):

	class Meta:
		model = Candidate
		fields = ('post', 'why_apply', 'why_vote', 'election_type')


class DepartmentForm(forms.ModelForm):

	class Meta:
		model = Department
		fields = ('name',)


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('name',)


class ElectionForm(forms.ModelForm):

	class Meta:
		model = Election
		fields = ('duedate', 'department', 'year', 'election_type')


	



		