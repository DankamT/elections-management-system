# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Department, Election, Student, Candidate, Post, FacultyElection, DepartmentElection, Exco

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Candidate)
admin.site.register(Post)
admin.site.register(FacultyElection)
admin.site.register(DepartmentElection)
admin.site.register(Exco)
admin.site.register(Election)

# Register your models here.
