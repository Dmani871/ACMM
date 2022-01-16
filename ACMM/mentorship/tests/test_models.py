from django.test import TestCase
from mentorship import models
from . import factories

class MentorTestCase(TestCase):
    def create_mentor(self,
        email = 'john.doe@mail.com',
        first_name = 'John',
        last_name = 'Doe',
        sex ='M',
        year_applied='A2',
        hear_about_us = 'WM',
        entrance_exam_experience = ['UKCAT'],
        interview_experience =  ['P'],
        area_of_support = ['PS'],
        occupation ='MD'):


        return models.MentorProfile.objects.create(
            email=email,first_name=first_name,last_name=last_name,sex=sex,
            year_applied=year_applied,hear_about_us =hear_about_us,
            entrance_exam_experience=entrance_exam_experience,
            interview_experience=interview_experience,
            area_of_support=area_of_support,
            occupation=occupation)

    def test_create_mentor(self):
        m = self.create_mentor()
        self.assertTrue(isinstance(m, models.MentorProfile))
        self.assertEqual(m.__str__(),m.occupation+"-"+m.email)

class MenteeTestCase(TestCase):
    def create_mentee(self,
        email = 'jane.doe@mail.com',
        first_name = 'Jane',
        last_name = 'Doe',
        sex ='F',
        year_applied='A2',
        hear_about_us = 'WM',
        entrance_exam_experience = ['UKCAT'],
        interview_experience =  ['P'],
        area_of_support = ['PS'],
        course='M',
        mentor_need="I want a mentor because ...",
        mentor_help="Help me with ...",
        mentor_relationship="I will build a relationship by ..."
        ):


        return models.MenteeProfile.objects.create(
            email=email,first_name=first_name,last_name=last_name,sex=sex,
            year_applied=year_applied,hear_about_us =hear_about_us,
            entrance_exam_experience=entrance_exam_experience,
            interview_experience=interview_experience,
            area_of_support=area_of_support,
            course=course,
            mentor_need=mentor_need,
            mentor_help=mentor_help,
            mentor_relationship=mentor_relationship
            )

    def test_create_mentee(self):
        m = self.create_mentee()
        self.assertTrue(isinstance(m, models.MenteeProfile))
        self.assertEqual(m.__str__(),m.course+"-"+m.email)
    
class MentorQualificationTestCase(TestCase):
    def create_qualification(self, name ='Biology',education_level='AS'):
        m=factories.MentorFactory.build()
        m.save()
        return models.MentorQualification.objects.create(name=name,education_level=education_level,profile=m)


    def test_create_qualification(self):
        q = self.create_qualification()
        self.assertTrue(isinstance(q, models.MentorQualification))
        self.assertEqual(q.__str__(),q.name+"-"+q.education_level)


class MenteeQualificationTestCase(TestCase):
    def create_qualification(self, name ='Biology',education_level='AS',grade='A',predicted=True):
        m=factories.MenteeFactory.build()
        m.save()
        return models.MenteeQualification.objects.create(name=name,education_level=education_level,grade=grade,predicted=predicted,profile=m)


    def test_create_qualification(self):
        q = self.create_qualification()
        self.assertTrue(isinstance(q, models.MenteeQualification))
        self.assertEqual(q.__str__(),q.name+"-"+q.education_level)