# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.urls import reverse


from django.contrib.auth.models import User

# Create your models here.

ELECTION_TYPE = (
        ('FA', 'Faculty'),
        ('DE', 'Department'),
    )


class Department(models.Model):
	name = models.CharField(max_length=30, help_text="Enter a department name (e.g. electrical and electronics engineering, computer engineering etc.)")
	# Foreign Key used because department can only belong to a faculty, but faculties can have multiple departments

	def __str__(self):
		return self.name
	

class Student(models.Model):
	firstname = models.CharField(max_length=50, help_text="Your first name (e.g. Ytembe etc.)", null=True)
	lastname = models.CharField(max_length=50, help_text="Your other names (e.g. Dankam Therese etc.)", null=True)
	fathername = models.CharField(max_length=50, help_text="Father's name (e.g. Dankam Celestin etc.)", null=True)
	mothername = models.CharField(max_length=50, help_text="Mother's name (e.g. Dankam Pauline etc.)", null=True)
	matricule = models.CharField(primary_key=True, max_length=10, help_text="Your matricule (e.g. FE14A221  etc.)", unique=True )
	department = models.ForeignKey('Department', help_text="Choose a department", null=False)
	picture = models.ImageField(upload_to='profile_images', help_text="upload a profile pic", blank=True)
	dateofbirth = models.DateField(null=True, help_text="(e.g. 1997-02-07)")
	status = models.NullBooleanField()

	def __str__(self):
		return "%s %s %s" % (self.firstname, self.matricule, self.department)

	def get_absolute_url(self):
		return reverse('student-details', args=[str(self.id)])

class Candidate(models.Model):
    student = models.ForeignKey('Student', null=False)
    votes = models.IntegerField(null=False, default=0)
    why_vote = models.TextField(null=False, help_text="Enter reasons why we should vote for you", default="I promise to look for internship" )
    why_apply = models.TextField(null=False, help_text="Enter reasons why you choose to be an exco", default="I promise to look for internship")
    post = models.ForeignKey('Post', null=False)
    department = models.ForeignKey('Department', null=False)
    election_type = models.CharField(max_length=10, null=False, choices=ELECTION_TYPE)
    status = models.NullBooleanField()
    def details(self):
		return (self.student, self.post, self.whyapply, self.whyvote, self.department)


class Election(models.Model):
    duedate = models.DateField(null=True)
    election_type = models.CharField(max_length=10, null=False, choices=ELECTION_TYPE)
    year = models.CharField(max_length=10, null=True)
    department = models.ForeignKey('Department', null=False)
    def __str__(self):
		return "%s %s %s" % (self.election_type, self.year, self.department)

		


class Post(models.Model):
	name = models.CharField(max_length=50, help_text="Enter a post (e.g. departmental president, faculty president  etc.)", unique=True)

	def __str__(self):
		return self.name



class FacultyElection(models.Model):
	post = models.ForeignKey('Post', null=False)
	student = models.ForeignKey('Student', null=False)

	


class DepartmentElection(models.Model):
	post = models.ForeignKey('post', null=False)
	department = models.ForeignKey('Department', null=False)
	student = models.ForeignKey('Student', null=False)
	
	

class Exco(models.Model):
	post = models.ForeignKey('Post', null=False)
	student = models.ForeignKey('Student', null=False)
	election = models.ForeignKey('Election', null=False)

	"""docstring for Excos"models.Modelf 
	__init__(self, arg):
		super(Excos,models.Model._
		_init__()
		self.arg = arg
	"""
		
		
		
"""class Administrator(models.Model):
	name = models.CharField(max_length=20, help_text="Enter a name (e.g. Elie Fute)")
	matricule = models.CharField(max_length=10, help_text="Enter a matricule (e.g. AD123  etc.)", unique=True)

	def __str__(self):
		return self.matricule

	docstring for Admin"models.Modelf __init__(self, arg):

		super(Admin,models.Model.__init__()

		self.arg = arg
	"""

