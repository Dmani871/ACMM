from django.test import TestCase
from mentorship import forms


class AddMentorFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MentorForm(data={
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertTrue(form.is_valid())
    def test_area_of_support_required(self):
        form = forms.MentorForm(data={
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
    def test_interview_experience_required(self):
        form = forms.MentorForm(data={
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
    def test_entrance_exam_experience_not_required(self):
        form = forms.MentorForm(data={
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertTrue(form.is_valid())

