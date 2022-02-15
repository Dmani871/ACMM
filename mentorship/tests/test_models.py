from django.test import TestCase
from mentorship import models

class MentorTest(TestCase):

    def setUp(self):
        self.mentor = models.MentorProfile.objects.create(
            email = 'john.doe@mail.com',
            first_name = 'John',
            last_name = 'Doe',
            sex ='M',
            year_applied='A2',
            hear_about_us = 'WM',
            entrance_exam_experience = ['UKCAT'],
            interview_experience =  ['P'],
            area_of_support = ['PS'],
            occupation ='MD')

    def test_mentor(self):
        self.assertTrue(isinstance(self.mentor, models.MentorProfile))

    def test_mentor_str_representation(self):
        self.assertEqual(str(self.mentor),"MD-john.doe@mail.com")

class MenteeTest(TestCase):

    def setUp(self):
        self.mentee = models.MenteeProfile.objects.create(
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
            mentor_relationship="I will build a relationship by ...")

    def test_mentee(self):
        self.assertTrue(isinstance(self.mentee, models.MenteeProfile))