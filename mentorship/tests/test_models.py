from django.test import TestCase
from ACMM.mentorship import models


class MentorTest(TestCase):

    def setUp(self):
        self.mentor = models.MentorProfile.objects.create(
            email='john.doe@mail.com',
            first_name='John',
            last_name='Doe',
            sex='M',
            year_applied='A2',
            hear_about_us='WM',
            entrance_exam_experience=['UCAT'],
            interview_experience=['P'],
            area_of_support=['PS'],
            occupation='MD')

    def test_mentor(self):
        self.assertTrue(isinstance(self.mentor, models.MentorProfile))

    def test_mentor_str_representation(self):
        self.assertEqual(str(self.mentor), "MD-john.doe@mail.com")


class MenteeTest(TestCase):

    def setUp(self):
        self.mentee = models.MenteeProfile.objects.create(
            email='jane.doe@mail.com',
            first_name='Jane',
            last_name='Doe',
            sex='F',
            year_applied='A2',
            hear_about_us='WM',
            entrance_exam_experience=['UKCAT'],
            interview_experience=['P'],
            area_of_support=['PS'],
            course='M',
            mentor_need="I want a mentor because ...",
            mentor_help="Help me with ...",
            mentor_relationship="I will build a relationship by ...")

    def test_mentee(self):
        self.assertTrue(isinstance(self.mentee, models.MenteeProfile))

    def test_mentee_str_representation(self):
        self.assertEqual(str(self.mentee), "M-jane.doe@mail.com")


class MentorQualificationTestCase(TestCase):

    def setUp(self):
        self.mentor = models.MentorProfile.objects.create(
            email='john.doe@mail.com',
            first_name='John',
            last_name='Doe',
            sex='M',
            year_applied='A2',
            hear_about_us='WM',
            entrance_exam_experience=['UKCAT'],
            interview_experience=['P'],
            area_of_support=['PS'],
            occupation='MD')
        self.mentor.save()
        self.qualification = models.MentorQualification.objects.create(
            name='Biology',
            education_level='AS',
            profile=self.mentor)

    def test_create_qualification(self):
        self.assertTrue(isinstance(self.qualification, models.MentorQualification))

    def test_mentor_qualification_str_representation(self):
        self.assertEqual(str(self.qualification), "AS-Biology")


class MenteeQualificationTestCase(TestCase):
    def setUp(self):
        self.mentee = models.MenteeProfile.objects.create(
            email='jane.doe@mail.com',
            first_name='Jane',
            last_name='Doe',
            sex='F',
            year_applied='A2',
            hear_about_us='WM',
            entrance_exam_experience=['UCAT'],
            interview_experience=['P'],
            area_of_support=['PS'],
            course='M',
            mentor_need="I want a mentor because ...",
            mentor_help="Help me with ...",
            mentor_relationship="I will build a relationship by ...")
        self.mentee.save()
        self.qualification = models.MenteeQualification.objects.create(
            name='Biology',
            education_level='AS',
            grade='A',
            predicted=True,
            profile=self.mentee)

    def test_create_qualification(self):
        self.assertTrue(isinstance(self.qualification, models.MenteeQualification))

    def test_mentor_qualification_str_representation(self):
        self.assertEqual(str(self.qualification), "AS-Biology")
