import json
from datetime import datetime
from xml.dom.minidom import parseString

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

from brownfield_django.main.models import Course, UserProfile, Document, Team
from brownfield_django.main.forms import CourseForm, TeamForm, CreateAccountForm
from brownfield_django.mixins import LoggedInMixin, LoggedInMixinSuperuser, \
    LoggedInMixinStaff, JSONResponseMixin



'''Moved Views From NEPI Over to Start With'''

class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user.pk)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('register'))

        if user_profile.is_student():
            url = '/student/%s/' % (user_profile.id)
        if user_profile.is_teacher():
            url = '/teacher/%s/' % (user_profile.id)

        return HttpResponseRedirect(url)


class RegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = CreateAccountForm
    success_url = '/account_created/'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)



DEMO_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
    <config>
            <user access="admin"/>

        <user realname="Team Joe Bob" 
              signedcontract="true" 
              startingbudget="60000"
              />
        <narrative enabled="True"/>
        <information>
            <info type="doc" name="policeReport" />
        </information>
    </config>
    <testdata>
        <test x="0" y="0" n="8" />
        <test x="0" y="0" n="9" z="10" />
        <test x="6" y="6" n="8" paramstring="blurdy blurd" />
        <test x="0" y="2" n="8" />
        <test x="1" y="4" n="8" />
    </testdata>
    <budget>
        <i a="1500" t="2004/08/30/23/11" d="excavation at 0,0" />
        <i a="1500" t="2004/08/30/23/12" d="excavation at 0,2" />
        <i a="200" t="2004/08/30/23/14" d="sgsa at 0,0" />
        <i a="200" t="2004/08/30/23/15" d="sgsa at 1,4" />
        <i a="1" t="2004/08/31/23/15" d="Questioned Al Milankovitch" />
    </budget>
</bfaxml>
"""


BROWNFIELD_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
  <config>
    <user realname="${record.name}" 
      signedcontract="true" 
      startingbudget="${int(record.course.startingBudget)}" 
      py:attrs="{'access':record.access}"
      />
    <narrative enabled="${record.course.enableNarrative}" />
    <information>
      <info py:for="i in record.info" type="${i.infoType}" name="${i.internalName}"/> 
    </information>
  </config>
  <testdata>
    <test py:for="t in record.tests"
      py:attrs="{'paramstring':t.paramString,'z':t.z}" 
      x="${t.x}" 
      y="${t.y}" 
      n="${t.testNumber}" />
  </testdata>
  <budget>
    <i py:for="t in record.history"
       a="${int(t.cost or 0)}" 
       t="${t.date and t.date.strftime('%Y/%m/%d/%H/%M')}" 
       d="${t.description}" />
  </budget>
</bfaxml>
 """





'''I am using this view to play around with getting the
flash to run'''
class BrownfieldDemoView(View):
    '''Initial view/controller usese templates play, bfaxml
    think like in ssnm it has one page and a second call to the flash app
    base template: play
    over template bfaxml
     
    Added xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    to html header - not sure if I need it
    '''
    template_name = 'main/demo.html'
    success_url = '/'

    def get(self, request):
        return render(request, 'main/flvplayer.html',
            content_type="application/xhtml+xml")


def get_demo(request):
    return HttpResponse(DEMO_XML)
    #return render(request, 'main/flvplayer.html', {'demo': DEMO_XML}, content_type="application/xhtml+xml")

def get_bfa(request):
    '''Flash is making calls to demo/media/flash/bfa.swf
    so we will give it'''
    return render(request, 'main/bfa.swf', content_type="application/xhtml+xml") 

def get_demo_history(request):
    return HttpResponse(DEMO_XML)

INFO_TEST = """
        <information>
            <info type="doc" name="policeReport" />
        </information>
"""

def get_demo_info(request):
    return HttpResponse(DEMO_XML)

def get_demo_test(request):
    return HttpResponse("<data><response>OK</response></data>")

def demo_save(request):
    return HttpResponse("<data><response>OK</response></data>")
        

class DemoHomeView(View):
    '''Again I'm just using this view to get the Flash working,
    no permissions or users'''
    template_name = 'main/demo_layout.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DemoHomeView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['documents'] = Document.objects.all()
        return context


class StudentHomeView(DetailView):
    '''In old application, students are shown a welcome message,
    followed by the instructor's email, and may join or leave teams'''
    model = UserProfile
    template_name = 'main/student_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(StudentView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['documents'] = Document.objects.all()
        return context


class TeamView(DetailView):
    '''If team has signed their contract they are allowed to play,
    if they have not signed their contract they are redirected
    to the sign contract page.
    the old play page url is: /course/%s/team/%s/play
    the old contract url is: /course/%s/team/%s/contract
    
    @expose(template='kid:brownfield.templates.bfaxml',
            content_type='application/xml',
            accept_format='application/xml',
            fragment=True, #so kid doesn't serve a DOCTYPE HTML declaration
            )
    @expose(template='kid:restresource.templates.view')
    @expose(template='json', accept_format='text/javascript')
    @require_owns_resource()    
    '''
    model = Team
    template_name = 'main/team_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['course_form'] = CourseForm()
        context['documents'] = Document.objects.all()
        return context


'''This should probably be a ListView'''


class TeacherView(DetailView):

    model = UserProfile
    template_name = 'main/instructor/instructor_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['course_form'] = CourseForm()
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        course_form = CourseForm(self.request.POST)

        if course_form.is_valid():
            course_form.save()
            messages.add_message(self.request, messages.INFO,
                                 'Your changes have been saved.')

            return HttpResponseRedirect('/dashboard/#course-list')

        context = self.get_context_data(object=self.object)
        context['course_form'] = course_form
        return self.render_to_response(context)


class TeacherCourseDetail(DetailView, UpdateView):

    model = Course
    template_name = 'main/instructor/course_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherCourseDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherCourseDetail, self).get_context_data(**kwargs)
        # course documents
        # message
        # course form
        # close course
        # special actions
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
