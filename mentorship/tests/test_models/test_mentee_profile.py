from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from itertools import product
from freezegun import freeze_time
import datetime as dt
import re

from django.db.utils import IntegrityError

from mentorship.models import MenteeProfile


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
        "terms_policy_consent": True,
        "date_joined": timezone.now(),
        "hear_about_us": "SM",
        "mentor_need": "Need mentoring for personal statement writing.",
        "mentor_help": "Can help with interview preparation.",
        "mentor_relationship": "Foster relationship by being proactive",
        "course": "M",
        "current_application": True,
        "accepted": False,
        "commitment": True,
        "state_educated": False,
        "family_support": True,
    }


import unittest
from parameterized import parameterized


def sum_even_numbers(numbers):
    return sum(filter(lambda x: x % 2 == 0, numbers))


class MenteeProfileTestCase(TestCase):
    BOOLEAN_FIELDS = [
        "wp_scheme",
        "applied_before",
        "contact_consent",
        "terms_policy_consent",
        "current_application",
        "accepted",
        "commitment",
        "state_educated",
        "family_support",
    ]

    def setUp(self):
        self.mentee_profile = MenteeProfile.objects.create(**mock_data())

    def test_mentee_profile_creation(self):
        mentee = self.mentee_profile
        self.assertEqual(mentee.first_name, "John")
        self.assertEqual(mentee.last_name, "Doe")
        self.assertEqual(mentee.personal_email, "test@example.com")
        self.assertEqual(mentee.number, "1234567890")
        self.assertEqual(mentee.year_applied, "A2")
        self.assertEqual(mentee.entrance_exam_experience, ["BMAT", "UCAT"])
        self.assertEqual(mentee.interview_experience, ["P", "M"])
        self.assertEqual(mentee.area_of_support, ["PS", "EE"])
        self.assertTrue(mentee.wp_scheme)
        self.assertFalse(mentee.applied_before)
        self.assertTrue(mentee.contact_consent)
        self.assertTrue(mentee.terms_policy_consent)
        self.assertEqual(mentee.hear_about_us, "SM")
        self.assertEqual(
            mentee.mentor_need, "Need mentoring for personal statement writing."
        )
        self.assertEqual(mentee.mentor_help, "Can help with interview preparation.")
        self.assertEqual(
            mentee.mentor_relationship, "Foster relationship by being proactive"
        )
        self.assertEqual(mentee.course, "M")
        self.assertTrue(mentee.current_application)
        self.assertFalse(mentee.accepted)
        self.assertTrue(mentee.commitment)
        self.assertFalse(mentee.state_educated)
        self.assertTrue(mentee.family_support)

    @parameterized.expand(["invalid-email", "test@.com" "@s.coms"])
    def test_email_validation_invalid_values(self, email):
        mentee_data = mock_data()
        mentee_data["personal_email"] = email
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    @freeze_time("2012-01-14")
    def test_date_joined_defaults_to_now(self):
        mentee_data = mock_data()
        del mentee_data["date_joined"]
        with freeze_time("2012-01-14"):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()
            value = getattr(mentee, "date_joined")
        self.assertEqual(value, dt.datetime(2012, 1, 14, tzinfo=dt.timezone.utc))

    @parameterized.expand(BOOLEAN_FIELDS)
    def test_defaults_to_false(self, field):
        mentee_data = mock_data()
        del mentee_data[field]

        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        value = getattr(mentee, field)
        self.assertFalse(value)

    @parameterized.expand(product(BOOLEAN_FIELDS, [False, True]))
    def test_boolean_field_valid_values(self, field, value):
        mentee_data = mock_data()
        mentee_data[field] = value

        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        db_value = getattr(mentee, field)
        self.assertEqual(value, db_value)

    @parameterized.expand(product(BOOLEAN_FIELDS, ["alse", 2, "invalid"]))
    def test_boolean_field_invalid_value(self, field, value):
        mentee_data = mock_data()
        mentee_data[field] = value

        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    @parameterized.expand(["M", "D"])
    def test_course_valid_options(self, value):
        mentee_data = mock_data()
        mentee_data["course"] = value
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertEqual(mentee.course, value)

    @parameterized.expand(["!", "d"])
    def test_course_invalid_options(self, value):
        mentee_data = mock_data()
        mentee_data["course"] = value
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    @parameterized.expand(["A2", "GRAD", "OT"])
    def test_year_applied_valid_options(self, value):
        mentee_data = mock_data()
        mentee_data["year_applied"] = value
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertEqual(mentee.year_applied, value)

    @parameterized.expand(["A22", "GRD", "wrong"])
    def test_year_appliedinvalid_options(self, value):
        mentee_data = mock_data()
        mentee_data["year_applied"] = value
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    @parameterized.expand(["WM", "C", "SM", "SU", "E", "OT"])
    def test_hear_about_us_valid_options(self, value):
        mentee_data = mock_data()
        mentee_data["hear_about_us"] = value
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertEqual(mentee.hear_about_us, value)

    @parameterized.expand(["wM", "sC", "MS", "12", "I", "No"])
    def test_hear_about_us_invalid_options(self, value):
        mentee_data = mock_data()
        mentee_data["hear_about_us"] = value
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    @parameterized.expand(
        [
            "personal_email",
            "first_name",
            "last_name",
            "number",
        ]
    )
    def test_required_field_missing(self, field):
        mentee_data = mock_data()
        del mentee_data[field]
        error_message_regex = re.escape(
            f'null value in column "{field}" of relation "mentorship_menteeprofile" violates not-null constraint'
        )

        with self.assertRaisesRegex(IntegrityError, error_message_regex) as e:
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    def test_encryption_storage(self):
        mentee_data = mock_data()

        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT personal_email,first_name,last_name,number FROM mentorship_menteeprofile WHERE id = %s",
                [self.mentee_profile.id],
            )
            raw_value = cursor.fetchone()
        personal_email, first_name, last_name, number = raw_value
        self.assertNotEqual(personal_email, mentee_data["personal_email"])
        self.assertNotEqual(first_name, mentee_data["first_name"])
        self.assertNotEqual(last_name, mentee_data["last_name"])
        self.assertNotEqual(number, mentee_data["number"])

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
        mentee_data = mock_data()
        mentee_data["entrance_exam_experience"] = choices
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertCountEqual(choices, mentee.entrance_exam_experience)

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
        mentee_data = mock_data()
        mentee_data["entrance_exam_experience"] = choices
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

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
        mentee_data = mock_data()
        mentee_data["interview_experience"] = choices
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertCountEqual(choices, mentee.interview_experience)

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
        mentee_data = mock_data()
        mentee_data["interview_experience"] = choices
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

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
        mentee_data = mock_data()
        mentee_data["area_of_support"] = choices
        mentee = MenteeProfile.objects.create(**mentee_data)
        mentee.full_clean()
        self.assertCountEqual(choices, mentee.area_of_support)

    @parameterized.expand(
        [
            ([],),
            (["PS?"],),
            ([1],),
            (["PS", "I", "invalid"],),
        ]
    )
    def test_area_of_support_invalid_choices(self, choices):
        mentee_data = mock_data()
        mentee_data["area_of_support"] = choices
        with self.assertRaises(ValidationError):
            mentee = MenteeProfile.objects.create(**mentee_data)
            mentee.full_clean()

    def test_str_rep(self):
        self.assertEqual(str(self.mentee_profile), "M-test@example.com")
