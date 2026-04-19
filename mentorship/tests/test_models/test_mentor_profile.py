from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from itertools import product
from freezegun import freeze_time
import datetime as dt
import re

from parameterized import parameterized
from django.db.utils import IntegrityError

from mentorship.models import MentorProfile


def mock_data():
    return {
        "personal_email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "number": "1234567890",
        "year_applied": "A2",
        "entrance_exam_experience": ["BMAT", "UCAT"],
        "interview_experience": ["P", "M"],
        "area_of_support": ["PS", "EE"],
        "wp_scheme": True,
        "applied_before": False,
        "contact_consent": True,
        "tcs_consent": True,
        "date_joined": timezone.now(),
        "hear_about_us": "SM",
        "occupation": "MD",
        "is_active": False,
        "additional_info": "I want to help",
    }


class MentorProfileTestCase(TestCase):
    BOOLEAN_FIELDS = [
        "wp_scheme",
        "applied_before",
        "contact_consent",
        "tcs_consent",
        "is_active",
    ]

    def setUp(self):
        self.mentor_profile = MentorProfile.objects.create(**mock_data())

    def test_mentor_profile_creation(self):
        mentor = self.mentor_profile
        self.assertEqual(mentor.first_name, "John")
        self.assertEqual(mentor.last_name, "Doe")
        self.assertEqual(mentor.personal_email, "test@example.com")
        self.assertEqual(mentor.number, "1234567890")
        self.assertEqual(mentor.year_applied, "A2")
        self.assertEqual(mentor.entrance_exam_experience, ["BMAT", "UCAT"])
        self.assertEqual(mentor.interview_experience, ["P", "M"])
        self.assertEqual(mentor.area_of_support, ["PS", "EE"])
        self.assertTrue(mentor.wp_scheme)
        self.assertFalse(mentor.applied_before)
        self.assertTrue(mentor.contact_consent)
        self.assertTrue(mentor.tcs_consent)
        self.assertEqual(mentor.hear_about_us, "SM")
        self.assertEqual(mentor.additional_info, "I want to help")
        self.assertEqual(mentor.occupation, "MD")

    @parameterized.expand(["invalid-email", "test@.com" "@s.coms"])
    def test_email_validation_invalid_values(self, email):
        mentor_data = mock_data()
        mentor_data["personal_email"] = email
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @freeze_time("2012-01-14")
    def test_date_joined_defaults_to_now(self):
        mentor_data = mock_data()
        del mentor_data["date_joined"]
        with freeze_time("2012-01-14"):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()
            value = getattr(mentor, "date_joined")
        self.assertEqual(value, dt.datetime(2012, 1, 14, tzinfo=dt.timezone.utc))

    @parameterized.expand(BOOLEAN_FIELDS)
    def test_defaults_to_false(self, field):
        mentor_data = mock_data()
        del mentor_data[field]

        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        value = getattr(mentor, field)
        self.assertFalse(value)

    @parameterized.expand(product(BOOLEAN_FIELDS, [False, True]))
    def test_boolean_field_valid_values(self, field, value):
        mentor_data = mock_data()
        mentor_data[field] = value

        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        db_value = getattr(mentor, field)
        self.assertEqual(value, db_value)

    @parameterized.expand(product(BOOLEAN_FIELDS, ["alse", 2, "invalid"]))
    def test_boolean_field_invalid_value(self, field, value):
        mentor_data = mock_data()
        mentor_data[field] = value

        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(["MD", "D", "MS", "DS"])
    def test_occupation_valid_options(self, value):
        mentor_data = mock_data()
        mentor_data["occupation"] = value
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertEqual(mentor.occupation, value)

    @parameterized.expand(["!", "d", "ED", "DO"])
    def test_occupation_invalid_options(self, value):
        mentor_data = mock_data()
        mentor_data["occupation"] = value
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(["A2", "GRAD", "OT"])
    def test_year_applied_valid_options(self, value):
        mentor_data = mock_data()
        mentor_data["year_applied"] = value
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertEqual(mentor.year_applied, value)

    @parameterized.expand(["A22", "GRD", "wrong"])
    def test_year_applied_invalid_options(self, value):
        mentor_data = mock_data()
        mentor_data["year_applied"] = value
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(["WM", "C", "SM", "SU", "E", "OT"])
    def test_hear_about_us_valid_options(self, value):
        mentor_data = mock_data()
        mentor_data["hear_about_us"] = value
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertEqual(mentor.hear_about_us, value)

    @parameterized.expand(["wM", "sC", "MS", "12", "I", "No"])
    def test_hear_about_us_invalid_options(self, value):
        mentor_data = mock_data()
        mentor_data["hear_about_us"] = value
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(
        [
            "personal_email",
            "first_name",
            "last_name",
            "number",
        ]
    )
    def test_required_field_missing(self, field):
        mentor_data = mock_data()
        del mentor_data[field]
        error_message_regex = re.escape(
            f'null value in column "{field}" of relation "mentorship_mentorprofile" violates not-null constraint'
        )

        with self.assertRaisesRegex(IntegrityError, error_message_regex) as e:
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    def test_encryption_storage(self):
        mentor_data = mock_data()

        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT personal_email,first_name,last_name,number FROM mentorship_mentorprofile WHERE id = %s",
                [self.mentor_profile.id],
            )
            raw_value = cursor.fetchone()
        personal_email, first_name, last_name, number = raw_value
        self.assertNotEqual(personal_email, mentor_data["personal_email"])
        self.assertNotEqual(first_name, mentor_data["first_name"])
        self.assertNotEqual(last_name, mentor_data["last_name"])
        self.assertNotEqual(number, mentor_data["number"])

    @parameterized.expand(
        [
            (["BMAT"],),
            (["UCAT"],),
            (["GAMSAT"],),
            (["BMAT", "GAMSAT"],),
            (["UCAT", "GAMSAT"],),
            (["BMAT", "UCAT"],),
            (["BMAT", "UCAT", "GAMSAT"],),
        ]
    )
    def test_entrance_exam_valid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["entrance_exam_experience"] = choices
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertCountEqual(choices, mentor.entrance_exam_experience)

    @parameterized.expand(
        [
            ([],),
            ([1],),
            (["GAMSA"],),
            (["BMAT?", "GAMSAT"],),
            (["BMAT", "UCAT", "invalid"],),
        ]
    )
    def test_entrance_exam_invalid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["entrance_exam_experience"] = choices
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(
        [
            (["P"],),
            (["M"],),
            (["G"],),
            (["P", "G"],),
            (["M", "G"],),
            (["P", "M"],),
            (["P", "M", "G"],),
        ]
    )
    def test_entrance_exam_valid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["interview_experience"] = choices
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertCountEqual(choices, mentor.interview_experience)

    @parameterized.expand(
        [
            ([],),
            ([1],),
            (["PP"],),
            (["P?", "M"],),
            (["P", "M", "invalid"],),
        ]
    )
    def test_entrance_exam_invalid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["interview_experience"] = choices
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    @parameterized.expand(
        [
            (["PS"],),
            (["I"],),
            (["EE"],),
            (["WE"],),
            (["WE", "I"],),
            (["EE", "PS", "I"],),
            (["PS", "EE"],),
            (["PS", "I", "EE", "WE"],),
        ]
    )
    def test_area_of_support_valid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["area_of_support"] = choices
        mentor = MentorProfile.objects.create(**mentor_data)
        mentor.full_clean()
        self.assertCountEqual(choices, mentor.area_of_support)

    @parameterized.expand(
        [
            ([],),
            (["PS?"],),
            ([1],),
            (["PS", "I", "invalid"],),
        ]
    )
    def test_area_of_support_invalid_choices(self, choices):
        mentor_data = mock_data()
        mentor_data["area_of_support"] = choices
        with self.assertRaises(ValidationError):
            mentor = MentorProfile.objects.create(**mentor_data)
            mentor.full_clean()

    def test_str_rep(self):
        self.assertEqual(str(self.mentor_profile), "MD-test@example.com")
