import factory
import factory.fuzzy
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification

class UserFactory(factory.Factory):
    class Meta:
        model = MenteeProfile
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@example.com'.format(user.first_name, user.last_name).lower())
    sex = factory.fuzzy.FuzzyChoice(['M','F'])
    year_applied = factory.fuzzy.FuzzyChoice(['A2','GRAD'])
    hear_about_us = factory.fuzzy.FuzzyChoice(['WM','C','SM','SU','O'])
    entrance_exam_experience= factory.fuzzy.FuzzyChoice([['BMAT','GAMSAT','UKCAT'],['BMAT','UKCAT'],['GAMSAT','UKCAT'],['UKCAT'],['GAMSAT'],['BMAT']])
    interview_experience=factory.fuzzy.FuzzyChoice([['P'],['M'],['G'],['M','P'],['G','M'],['G','M','P']])
    area_of_support=factory.fuzzy.FuzzyChoice([['PS'],['I'],['EE'],['WE'],['I','PS'],['EE','I'],['PS','EE','WE']])
    course=factory.fuzzy.FuzzyChoice(['M','D'])
    mentor_need=factory.fuzzy.FuzzyText(length=200)
    mentor_help=factory.fuzzy.FuzzyText(length=200)
    mentor_relationship=factory.fuzzy.FuzzyText(length=200)

