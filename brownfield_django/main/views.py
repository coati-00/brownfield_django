import json
from datetime import datetime
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from brownfield_django.main.models import Course, UserProfile
from brownfield_django.main.forms import CourseForm, TeamForm


'''Moved Views From NEPI Over to Start With'''

class StudentHomePage(DetailView):

    model = UserProfile
    template_name = 'main/home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(StudentHomePage, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentHomePage, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        return context

'''This should probably be a ListView'''
class TeacherHomePage(DetailView):

    model = UserProfile
    template_name = 'main/home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherHomePage, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherHomePage, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['course_form'] = CourseForm()
        context['team_form'] = TeamForm()
        return context
#     def post(self, *args, **kwargs):
#         self.object = self.get_object()
#
#         profile_form = UpdateProfileForm(self.request.POST)
#
#         if profile_form.is_valid():
#             profile_form.save()
#             url = '/%s-dashboard/%s/#user-profile' % (
#                 self.request.user.profile.role(), self.request.user.profile.id)
#             return HttpResponseRedirect(url)
#
#         context = self.get_context_data(object=self.object)
#         context['profile_form'] = profile_form
#         return self.render_to_response(context)


class TeacherCourseDetail(DetailView, UpdateView):

    model = Course
    template_name = 'main/course_detail.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherCourseDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherCourseDetail, self).get_context_data(**kwargs)
        context['course_form'] = CourseForm()
        context['team_form'] = TeamForm()
        return context
#     def post(self, *args, **kwargs):
#         self.object = self.get_object()
#
#         profile_form = UpdateProfileForm(self.request.POST)
#
#         if profile_form.is_valid():
#             profile_form.save()
#             url = '/%s-dashboard/%s/#user-profile' % (
#                 self.request.user.profile.role(), self.request.user.profile.id)
#             return HttpResponseRedirect(url)
#
#         context = self.get_context_data(object=self.object)
#         context['profile_form'] = profile_form
#         return self.render_to_response(context)
