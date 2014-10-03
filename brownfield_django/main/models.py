import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


PROFILE_CHOICES = (
    ('AD', 'Administrator'),
    ('TE', 'Teacher'),
    ('ST', 'Student'),
)


'''
Old Tables:
             "Visit",
             "User",
             "VisitIdentity",
             "Permission",
             "Group",
             "Document",
             "Course",
             "Team",
             "Student",
             "History",
             "PerformedTest",
             "Information",
'''


class Course(models.Model):
    '''
    Course Model - I added an archive field to indicate if a
    course should be excluded from the Dashboard, without necessarily
    deleting all of the data in case it is needed at a later time.

    Added creator field but since only admins will be allowed to view
    everyone's courses, and since they may create a course on a professor's
    behalf, I changed it to be a professor/instructor field.
    '''
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, default='')
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    message = models.TextField(max_length=255, default='')
    active = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    professor = models.ForeignKey(User, related_name="taught_by", null=True,
                                  default=None, blank=True)

    def __unicode__(self):
        return self.name

    def get_students(self):
        participants = UserProfile.objects.filter(course=self)
        # need to exclude teacher
        return participants

    def get_teams(self):
        teams = Team.objects.filter(course=self)
        return teams

    def get_documents(self):
        documents = Document.objects.filter(course=self)
        return documents

    def get_course_form(self):
        form = CourseForm()
        return form


class CourseForm(ModelForm):
    class Meta:
        model = Course


class Document(models.Model):
    course = models.ForeignKey(Course, null=True,
                               default=None, blank=True)
    name = models.CharField(max_length=255, default='')
    link = models.CharField(max_length=255, default='')
    visible = models.BooleanField(default=False)
    # in old application content is href not sure if it should be but...


class Team(models.Model):
    '''Team: A team will have one login/username
    All accounting/history/actions is by team.
    SINCE USER PROFILE IS A TEAM DO WE NEED TO
    MAKE THIS HAVE A RELATION TO USER< OR JUST USE
    THIS TO STORE USER TYPE TEAM DATA?
    '''
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)
    team_entity = models.OneToOneField(User)
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)

    class Meta:
        '''We don't want teams with the same name in a course'''
        ordering = ['name']
        unique_together = ['name', 'course']

    def __unicode__(self):
        return self.name

    def get_members(self):
        try:
            members = self.userprofile_set.all()
            return members
        except:
            return None

    def get_signed_contract(self):
        return self.signed_contract

    def get_course(self):
        return self.course


class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a team, course,
    and course progress.'''
    user = models.OneToOneField(User, related_name="profile")
    # interactive = models.ForeignKey(Interactive, null=True, blank=True)
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]

    def display_name(self):
        return self.user.username

    def is_student(self):
        return self.profile_type == 'ST'

    def is_teacher(self):
        return self.profile_type == 'TE'

    def is_admin(self):
        return self.profile_type == 'AD'

    def role(self):
        if self.is_student():
            return "student"
        elif self.is_teacher():
            return "faculty"
        elif self.is_adminr():
            return "administrator"


class History(models.Model):
    team = models.ForeignKey(Team)
    date = models.DateTimeField(default=datetime.datetime.now)
    description = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.description, self.team)


class PerformedTest(models.Model):
    X = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testNumber = models.IntegerField(default=0)
    paramString = models.CharField(max_length=255)

    def __unicode__(self):
        return self.paramString


class Visit(models.Model):
    pass
