import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers

from brownfield_django.main.views import CourseViewSet, UserViewSet, \
    DocumentViewSet
from brownfield_django.main.views import DetailJSONCourseView, \
    HomeView, AdminStudentView, \
    ActivateCourseView, EditCourseTeamsView, \
    AdminTeamView, CCNMTLHomeView, CCNMTLCourseDetail, \
    TeamHomeView, CreateTeamsView, CCNMTLViewTeamsDetail


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})


router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'user', UserViewSet)
router.register(r'document', DocumentViewSet)
router.register(r'document', DocumentViewSet, 'update')

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    (r'^$', HomeView.as_view()),
    (r'^ccnmtl/home/(?P<pk>\d+)/$', CCNMTLHomeView.as_view()),
    (r'^edit_course_teams/(?P<pk>\d+)/$', EditCourseTeamsView.as_view()),
    (r'^team/home/(?P<pk>\d+)/$', TeamHomeView.as_view()),
    (r'^team/$', AdminTeamView.as_view()),
    (r'^team/(?P<pk>\d+)$', AdminTeamView.as_view()),
    (r'^course_details/(?P<pk>\d+)/$', CCNMTLCourseDetail.as_view()),
    (r'^create_teams/(?P<pk>\d+)/$', CreateTeamsView.as_view()),
    (r'^activate_course/(?P<pk>\d+)$', ActivateCourseView.as_view()),
    # need to figure out url for students that doesn't not conflict with
    # dashboard urls
    # Teacher and Admin Views  CreateTeamsView
    (r'^update_course/(?P<pk>\d+)$', DetailJSONCourseView.as_view()),
    # (r'^activate_course/(?P<pk>\d+)/$', ActivateCourseView.as_view()),
    (r'^student/$', AdminStudentView.as_view()),
    (r'^student/(?P<pk>\d+)$', AdminStudentView.as_view()),
    (r'^current_teams/(?P<pk>\d+)/$', CCNMTLViewTeamsDetail.as_view()),
    # student/team views
    # Demo View
    (r'^demo/$', TemplateView.as_view(template_name="main/demo.html")),
    (r'^demo/play$', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    (r'^media/history/$', "brownfield_django.main.views.get_demo"),
    (r'^demo/media/flash/$', "brownfield_django.main.views.get_bfa"),
    # ([0-9]{15}\.[0-9]{15})
    # ([0-9]+) should it be ?cachebuster=(([0-9]+)(.?)([0-9]+))$ instead?
    # almost? url(r'^media/history/?cachebuster=(?\d+.?\d*)$',
    # DemoHomeView.as_view()),
    # url(r'^media/history/?cachebuster=(/d*.?d*/)$', DemoHomeView.as_view()),
    (r'^demo/info/$', "brownfield_django.main.views.get_demo_info"),
    (r'^demo/test/$', "brownfield_django.main.views.get_demo_test"),
    (r'^demo/save/$', "brownfield_django.main.views.demo_save"),
    (r'^visrecon/$', TemplateView.as_view(
        template_name="interactive/visrecon.html")),
    (r'^demo/$', TemplateView.as_view(
        template_name="interactive/demo_layout.html")),
    (r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
