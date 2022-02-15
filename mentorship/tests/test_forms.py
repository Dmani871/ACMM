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

    def test_labels(self):
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
        self.assertIn('<label for="id_email">Email:</label>', form.as_p())
        self.assertIn('<label for="id_first_name">First name:</label>', form.as_p())
        self.assertIn('<label for="id_last_name">Last name:</label>', form.as_p())
        self.assertIn('<label for="id_sex">Sex:</label>', form.as_p())
        self.assertIn('<label for="id_year_applied">Qualification level prior to studying Medicine/Dentistry:</label>',
                      form.as_p())
        self.assertIn('<label for="id_hear_about_us">How did you hear about us?</label>', form.as_p())
        self.assertIn('<label>What exam experience do you have?</label>', form.as_p())
        self.assertIn('<label>What interview experience do you have?</label>', form.as_p())
        self.assertIn('<label>What area can you provide support in?</label>', form.as_p())
        self.assertIn('<label for="id_occupation">Occupation:</label>', form.as_p())

class AddMentorQualificationFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MentorQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2'})
        self.assertTrue(form.is_valid())
    def test_name_required(self):
        form = forms.MentorQualificationForm(data={
            'education_level': 'A2'})
        self.assertFalse(form.is_valid())