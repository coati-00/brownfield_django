import json

# import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import Context
from django.views.generic import View
from django.views.generic.detail import DetailView

from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from brownfield_django.main.models import Course, UserProfile, Document, \
    Team, History
from brownfield_django.main.serializers import DocumentSerializer, \
    UserSerializer, TeamNameSerializer, CourseSerializer, \
    StudentUserSerializer, TeamSerializer, StudentMUserSerializer

from brownfield_django.main.xml_strings import INITIAL_XML, \
    TEAM_HISTORY
from brownfield_django.mixins import LoggedInMixin, JSONResponseMixin


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned courses
        filtering against the request.user
        excluding against an `exclude_username` query parameter in the URL.
        """
        if self.request.user.profile.is_student():
            return Course.objects.none()

        queryset = Course.objects.filter(archive=False)

        if self.request.user.profile.is_teacher():
            return queryset.filter(professor=self.request.user)

        if self.request.user.profile.is_admin():
            exclude = self.request.QUERY_PARAMS.get('exclude_username', None)
            if exclude is not None:
                queryset = queryset.exclude(professor__username=exclude)
            else:
                queryset = queryset.filter(professor=self.request.user)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.profile.is_student():
            return User.objects.get(id=self.request.user.id)
        else:
            return User.objects.all()


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def update(self, request, pk=None):
        document = Document.objects.get(id=pk)
        if document.visible is True:
            document.visible = False
        elif document.visible is False:
            document.visible = True
        document.save()
        return Response(document.visible, status.HTTP_200_OK)

    def get_queryset(self):
        '''
        Form Docs: queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.
        '''
        course_pk = self.request.QUERY_PARAMS.get('course', None)
        if course_pk is not None:
            queryset = Document.objects.filter(course__pk=course_pk)
        else:
            queryset = Document.objects.none()
        return queryset


class StudentViewSet(viewsets.ModelViewSet):
    '''Attempting to redo Student Ajax handling
    the correct way with a model viewset - still very wrong.'''
    queryset = User.objects.filter(profile__profile_type='ST')
    serializer_class = StudentUserSerializer

    def create(self, request):
        try:
            key = self.request.QUERY_PARAMS.get('course', None)
            course = Course.objects.get(pk=key)
            username = str(request.DATA['first_name']) + \
                str(request.DATA['last_name'])
            student = User.objects.create_user(
                username=username,
                first_name=request.DATA['first_name'],
                last_name=request.DATA['last_name'],
                email=request.DATA['email'])
            new_profile = UserProfile.objects.create(course=course,
                                                     user=student,
                                                     profile_type='ST')
            new_profile.save()
            serializer = StudentMUserSerializer(student)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        student = get_object_or_404(User, pk=pk)
        #.objects.get(pk=pk)
        student.first_name = request.DATA['first_name']
        student.last_name = request.DATA['last_name']
        student.email = request.DATA['email']
        student.save()
        serializer = StudentUserSerializer(
            data=request.DATA)
        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)
        elif serializer.is_valid() is False:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        student = User.objects.get(pk=pk)
        student.delete()
        return Response(status.HTTP_200_OK)

    def get_queryset(self):
        course_pk = self.request.QUERY_PARAMS.get('course', None)
        if course_pk is not None:
            students = UserProfile.objects.filter(course__pk=course_pk,
                                                  profile_type='ST')
            queryset = User.objects.filter(profile__in=students)
        else:
            '''Is it safe to assume there are no students
            if something goes wrong.'''
            queryset = User.objects.none()
        return queryset


class AdminTeamView(APIView):
    """
    This view interacts with backbone to allow instructors to
    view and add teams to their course. Will also probably be where
    logic for keeping track of which students are where will be.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, *args, **kwargs):
        '''Send back all teams currently in course.'''
        course = self.get_object(pk)
        try:
            teamprofiles = course.get_teams()
            teams = User.objects.filter(team__in=teamprofiles)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)
        except:
            '''Assume collection is currently empty'''
            return Response(status.HTTP_200_OK)

    def post(self, request, pk, format=None, *args, **kwargs):
        '''
        Add a team.
        Team creation is where we set the team
        budgets so they are all the same.
        '''
        course = self.get_object(pk)
        team_name = request.DATA['username']
        password1 = request.DATA['password1']
        password2 = request.DATA['password2']
        if password1 == password2:
            user = User.objects.create_user(username=team_name,
                                            first_name=team_name,
                                            password=password1)
            team = Team.objects.create(
                user=user,
                course=course,
                budget=course.startingBudget,
                team_passwd=password1)
            team.save()  # saving bc pylint complains it is not used
            try:
                new_user = User.objects.get(username=team_name)
                serializer = TeamNameSerializer(new_user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except:
                pass
                # print 'could not find user'
        else:
            # print "passwords do not match"
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        team = User.objects.get(pk=pk)
        team.delete()
        return Response(status.HTTP_200_OK)


class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user.pk)
            if user_profile.is_teacher():
                url = '/ccnmtl/home/%s/' % (user_profile.id)
            if user_profile.is_admin():
                url = '/ccnmtl/home/%s/' % (user_profile.id)
        except UserProfile.DoesNotExist:
            pass  # we need to see if user is a team
            # '''We are not allowing users to register.'''
            # return HttpResponseForbidden("forbidden")
        try:
            team = Team.objects.get(user=request.user.pk)
            url = '/team/home/%s/' % (team.id)
        except:
            pass
        return HttpResponseRedirect(url)


class DetailJSONCourseView(JSONResponseMixin, View):
    '''
    For now I think it is best to have a separate view for the
    course detail template.
    '''

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def convert_TF_to_json(self, attribute):
        if attribute is True:
            return 'true'
        elif attribute is False:
            return 'false'

    def convert_TF_from_json(self, attribute):
        if attribute == 'true':
            return True
        elif attribute == 'false':
            return False

    def get(self, request, pk, format=None, *args, **kwargs):
        '''
        Should probably retrieve the information for the course here
        so it appears in the form/pre-populates the fields.
        '''
        course = self.get_object(pk)
        j_course = []
        j_course.append({'id': str(course.id),
                         'name': course.name,
                         'startingBudget': course.startingBudget,
                         'enableNarrative': self.convert_TF_to_json(
                             course.enableNarrative),
                         'message': course.message,
                         'active': self.convert_TF_to_json(course.active),
                         'archive': self.convert_TF_to_json(course.archive),
                         'professor': str(course.professor)
                         })
        return self.render_to_json_response({'course': j_course})

    def post(self, request, pk, format=None, *args, **kwargs):
        '''This is really really ugly as is get method need to clean up.'''
        course = self.get_object(pk)
        course.name = self.request.POST.get('name')
        course.startingBudget = int(self.request.POST.get('startingBudget'))
        course.enableNarrative = self.convert_TF_from_json(
            self.request.POST.get('enableNarrative'))
        course.message = self.request.POST.get('message')
        course.active = self.convert_TF_from_json(
            self.request.POST.get('active'))
        course.archive = self.convert_TF_from_json(
            self.request.POST.get('archive'))
        userprof = User.objects.get(
            username=self.request.POST.get('professor'))
        course.professor = userprof
        course.save()
        j_course = []
        j_course.append({'id': str(course.id),
                         'name': course.name,
                         'startingBudget': course.startingBudget,
                         'enableNarrative': self.convert_TF_to_json(
                             course.enableNarrative),
                         'message': course.message,
                         'active': self.convert_TF_to_json(course.active),
                         'archive': self.convert_TF_to_json(course.archive),
                         'professor': str(course.professor)
                         })
        return self.render_to_json_response({'course': j_course})


class ActivateCourseView(JSONResponseMixin, View):

    def send_student_email(self, student):
        template = loader.get_template(
            'main/ccnmtl/course_dash/student_activation_notice.txt')
        subject = "Welcome to Brownfield!"
        ctx = Context({'student': student, 'team': student.profile.team})
        message = template.render(ctx)
        '''who is the sender?'''
        sender = 'cdunlop@columbia.edu'  # settings.BNFD_MAIL
        send_mail(subject, message, sender, [student.email])

    def post(self, request, pk):
        '''This is really really ugly as is get method need to clean up.'''
        student_list = json.loads(request.POST['student_list'])
        for student in student_list:
            team = Team.objects.get(pk=student['student']['team_id'])
            student = User.objects.get(pk=student['student']['pk'])
            profile = UserProfile.objects.get(user=student)
            team.userprofile_set.add(profile)
            self.send_student_email(student)
        act_crs = Course.objects.get(pk=pk)
        act_crs.active = True
        act_crs.save()
        return self.render_to_json_response({'success': 'true'})


class EditTeamsView(View):

    def get(self, request, pk):
        template = loader.get_template(
            'main/ccnmtl/course_dash/team_form.html')
        course = Course.objects.get(pk=pk)
        ctx = Context({'object': course})
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class ShowTeamsView(View):

    def get(self, request, pk):
        template = loader.get_template(
            'main/ccnmtl/course_dash/team_table.html')
        course = Course.objects.get(pk=pk)
        ctx = Context({'object': course})
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class CCNMTLHomeView(DetailView):

    model = UserProfile
    template_name = 'main/ccnmtl/home_dash/ccnmtl_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(CCNMTLHomeView, self).dispatch(*args, **kwargs)


class CCNMTLCourseDetail(DetailView):

    model = Course
    template_name = 'main/ccnmtl/course_dash/course_home.html'
    success_url = '/'


'''Beginning of Team Views'''


class TeamHomeView(DetailView):

    model = Team
    template_name = 'main/team/team_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.team.id:
            return HttpResponseForbidden("forbidden")
        return super(TeamHomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamHomeView, self).get_context_data(**kwargs)
        course = Course.objects.get(pk=self.object.course.pk)
        context['document_list'] = course.document_set.filter(visible=True)
        return context


"""Views for interactive."""


class BrownfieldInfoView(View):
    '''Corresponds to "demo/info/"'''
    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse("<data><response>OK</response></data>")
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse("<data><response>OK</response></data>")
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)


class BrownfieldHistoryView(View):

    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)


class TeamHistoryView(View):
    """Need to parse the XML and substitute the correct
    values for each student interaction."""

    def send_history(self):
        pass
#     th = TEAM_HISTORY
#         print th
#         et = ET.fromstring(th)
#         print et
#         for each in et.iter('user'):
#             print each.attrib
#             each.set('signedcontract', team.signed_contract)
#             each.set('startingbudget', team.budget)
#             each.set('realname', team.user.username)

    def get(self, request, pk):
        """Get retrieves the current team values for the flash."""
        team = Team.objects.get(user=request.user)
        try:
            team_history = History.objects.get(team=team)
            team_history.save()  # flake8 says it is unused if not saved
            return HttpResponse(self.send_history())
        except:
            '''If there is no history record associated with,
            the team yet it is their first log in.'''
            return HttpResponse(TEAM_HISTORY)


class TeamInfoView(View):

    def post(self, request, pk):
        team = Team.objects.get(user=request.user)
        req_type = request.POST['infoType']

        if req_type == "recon":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            return HttpResponse("<data><response>OK</response></data>")

        elif req_type == "visit":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            th.save()
            return HttpResponse("<data><response>OK</response></data>")

        elif req_type == "question":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            return HttpResponse("<data><response>OK</response></data>")


class BrownfieldTestView(View):

    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_team():
            '''Get appropriate team record'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_team():
            '''Get appropriate team record'''
            return HttpResponse(INITIAL_XML)


class TeamPerformTest(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnLoad(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnSave(LoggedInMixin, JSONResponseMixin, View):
    pass
