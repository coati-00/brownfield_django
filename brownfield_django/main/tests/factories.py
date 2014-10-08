import factory
from datetime import datetime
from django.contrib.auth.models import User
from brownfield_django.main.models import Document, Course, \
    UserProfile, History, PerformedTest


'''
Adding initial factories for model tests, will do more after for views.
'''


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class CourseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existent students."
    active = True
    professor = factory.SubFactory(UserFactory)


class DocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Document
    name = "Test Document for Course"
    course = factory.SubFactory(CourseFactory)
    link = "<a href='/path/to/the/course/document/here'></a>"
    visible = False


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)
    profile_type = 'ST'
    course = factory.SubFactory(CourseFactory)


class TeamProfileFactory(UserProfileFactory):
    profile_type = 'TM'


class TeacherProfileFactory(UserProfileFactory):
    user = factory.SubFactory(UserFactory)
    profile_type = 'TE'


class AdminProfileFactory(UserProfileFactory):
    user = factory.SubFactory(UserFactory)
    profile_type = 'AD'


class CourseOneFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course One"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class CourseTwoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course Two"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class CourseThreeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course Two"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = History
    team = factory.SubFactory(TeamProfileFactory)
    date = datetime.now()
    description = "History Record"
    cost = 100


class PerformedTestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PerformedTest
    X = 10
    y = 30
    z = 60
    testNumber = 1
    paramString = '''Still need to find format for these...'''


'''Adding Users and UserProfiles/Students/Teams to add to Course
and/or Teams in test_models to see that it returns those Users.'''


class StudentUserFactoryOne(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "Student1"
    password = "Student1"


class StudentUserFactoryTwo(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "Student2"
    password = "Student2"


class ActualTeamUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "Test_Team"
    password = "Test_Team"


class StudentProfileFactoryOne(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(StudentUserFactoryOne)
    profile_type = 'ST'


class StudentProfileFactoryTwo(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(StudentUserFactoryTwo)
    profile_type = 'ST'


class NewTeamProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(ActualTeamUserFactory)
    profile_type = 'TM'
    course = factory.SubFactory(CourseFactory)


class StudentInTeamProfileFactoryOne(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(StudentUserFactoryOne)
    profile_type = 'ST'
    team_name = "TeamLabel"


class StudentInTeamProfileFactoryTwo(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(StudentUserFactoryTwo)
    profile_type = 'ST'
    team_name = "TeamLabel"


'''Creating Separate UserFactory and Profile for test_admin_views'''


class AdminUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "Admin"
    password = factory.PostGenerationMethodCall('set_password', "Admin")


class ViewsAdminProfileFactory(UserProfileFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(AdminUserFactory)
    profile_type = 'AD'


class AdminUserCourseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course"
    startingBudget = 100000
    enableNarrative = True
    message = "Hello you non existent students."
    active = True
    professor = factory.SubFactory(UserFactory)


class AdminUserDocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Document
    name = "Test Document for Admin"
    course = factory.SubFactory(CourseFactory)
    link = "<a href='/path/to/the/course/document/here'></a>"
    visible = False


'''Creating Separate UserFactory and Profile for test_teacher_views'''


class TeacherUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "Teacher"
    password = factory.PostGenerationMethodCall('set_password', "Teacher")


class ViewsTeacherProfileFactory(UserProfileFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(TeacherUserFactory)
    profile_type = 'TE'


'''Adding another User and new User's Courses to
test /user_courses/ vs /all_courses/'''


# class NewUserFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = User
#     username = factory.Sequence(lambda n: "user%d" % n)
#     password = factory.PostGenerationMethodCall('set_password', 'test')
#
#
# class CourseOneFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = Course
#     name = "Test Course One"
#     startingBudget = 65000
#     enableNarrative = True
#     message = "Hello you non existant students."
#     active = True
#     professor = factory.SubFactory(UserFactory)
#
#
# class CourseTwoFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = Course
#     name = "Test Course Two"
#     startingBudget = 65000
#     enableNarrative = True
#     message = "Hello you non existant students."
#     active = True
#     professor = factory.SubFactory(UserFactory)
#
#
# class CourseThreeFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = Course
#     name = "Test Course Two"
#     startingBudget = 65000
#     enableNarrative = True
#     message = "Hello you non existant students."
#     active = True
#     professor = factory.SubFactory(UserFactory)
