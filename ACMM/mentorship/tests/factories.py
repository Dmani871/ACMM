import factory
import factory.fuzzy
import random
from mentorship import models


class MenteeFactory(factory.Factory):
    class Meta:
        model = models.MenteeProfile
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@example.com'.format(user.first_name, user.last_name).lower())
    sex = factory.fuzzy.FuzzyChoice(['M','F'])
    year_applied = factory.fuzzy.FuzzyChoice(['A2','GRAD'])
    hear_about_us = factory.fuzzy.FuzzyChoice(['WM','C','SM','SU','O'])
    entrance_exam_experience= factory.fuzzy.FuzzyChoice([
        ['UKCAT'],
        ['GAMSAT'],
        ['BMAT'],
        ['BMAT','UKCAT'],
        ['BMAT','GAMSAT'],
        ['GAMSAT','UKCAT'],
        ['BMAT','GAMSAT','UKCAT']
        ])
    interview_experience=factory.fuzzy.FuzzyChoice([
        ['P'],
        ['M'],
        ['G'],
        ['G','P'],
        ['G','M'],
        ['M','P'],
        ['G','M','P']])
    area_of_support=factory.fuzzy.FuzzyChoice([
        ['PS'],
        ['I'],
        ['EE'],
        ['WE'],
        ['I','PS'],
        ['EE','I'],
        ['PS','EE','WE']])
    course=factory.fuzzy.FuzzyChoice(['M','D'])
    mentor_need=factory.fuzzy.FuzzyText(length=200)
    mentor_help=factory.fuzzy.FuzzyText(length=200)
    mentor_relationship=factory.fuzzy.FuzzyText(length=200)

    @factory.post_generation
    def qualifications(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.save()
        number_of_qualifications = random.randint(2, 4)
        for n in range(number_of_qualifications):
            q=MenteeQualificationFactory(profile=obj)
            q.save()

class MenteeQualificationFactory(factory.Factory):
    class Meta:
        model = models.MenteeQualification
    name = factory.fuzzy.FuzzyChoice([
        'Biology',
        'Chemisty',
        'Mathematics',
        'Further Mathematics',
        'Physics',
        'French',
        'Biomedical Science',
        'Psychology'])
    education_level= factory.fuzzy.FuzzyChoice(['AS','A2','IB','UG','M','D'])
    grade=factory.fuzzy.FuzzyChoice(["A*","A","B","C","D","E","F","1","2","3","4","5","6","7","1st","2:1","2:2","3rd"])
    profile = factory.SubFactory(MenteeFactory)

class MentorFactory(factory.Factory):
    class Meta:
        model = models.MentorProfile
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@example.com'.format(user.first_name, user.last_name).lower())
    sex = factory.fuzzy.FuzzyChoice(['M','F'])
    year_applied = factory.fuzzy.FuzzyChoice(['A2','GRAD'])
    hear_about_us = factory.fuzzy.FuzzyChoice(['WM','C','SM','SU','O'])
    entrance_exam_experience= factory.fuzzy.FuzzyChoice([
        ['UKCAT'],
        ['GAMSAT'],
        ['BMAT'],
        ['BMAT','UKCAT'],
        ['BMAT','GAMSAT'],
        ['GAMSAT','UKCAT'],
        ['BMAT','GAMSAT','UKCAT']
        ])
    interview_experience=factory.fuzzy.FuzzyChoice([
        ['P'],
        ['M'],
        ['G'],
        ['G','P'],
        ['G','M'],
        ['M','P'],
        ['G','M','P']])
    area_of_support=factory.fuzzy.FuzzyChoice([
        ['PS'],
        ['I'],
        ['EE'],
        ['WE'],
        ['I','PS'],
        ['EE','I'],
        ['PS','EE','WE']])
    occupation=factory.fuzzy.FuzzyChoice(['MD','D','MS','DS'])
    @factory.post_generation
    def qualifications(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.save()
        number_of_qualifications = random.randint(2, 4)
        for n in range(number_of_qualifications):
            q=MentorQualificationFactory(profile=obj)
            q.save()
   


class MentorQualificationFactory(factory.Factory):
    class Meta:
        model = models.MentorQualification
    name = factory.fuzzy.FuzzyChoice([
        'Biology',
        'Chemisty',
        'Mathematics',
        'Further Mathematics',
        'Physics',
        'French',
        'Biomedical Science',
        'Psychology'])
    education_level= factory.fuzzy.FuzzyChoice(['AS','A2','IB','UG','M','D'])
    profile = factory.SubFactory(MenteeFactory)
