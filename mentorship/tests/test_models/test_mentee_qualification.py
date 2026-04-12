from django.test import TestCase
from mentorship.models import MenteeQualification, MenteeProfile


class MenteeQualificationTestCase(TestCase):
    def setUp(self):
        self.mentee = MenteeProfile.objects.create(
            personal_email="jane.doe@mail.com",
            first_name="Jane",
            last_name="Doe",
            number="2",
            year_applied="A2",
            hear_about_us="WM",
            entrance_exam_experience=["UCAT"],
            interview_experience=["P"],
            area_of_support=["PS"],
            course="M",
            mentor_need="I want a mentor because ...",
            mentor_help="Help me with ...",
            mentor_relationship="I will build a relationship by ...",
        )
        self.mentee.save()
        self.qualification = MenteeQualification.objects.create(
            name="Biology",
            education_level="AS",
            grade="A",
            predicted=True,
            profile=self.mentee,
        )

    def test_create_qualification(self):
        self.assertTrue(isinstance(self.qualification, MenteeQualification))

    def test_mentor_qualification_str_representation(self):
        self.assertEqual(str(self.qualification), "AS-Biology")
