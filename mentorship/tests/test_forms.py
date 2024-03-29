from django.test import TestCase
from mentorship import forms


class AddMentorFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'work_email': 'john.doe@nhs.co.uk',
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

    def test_tcs_check_required(self):
        form = forms.MentorForm(data={
            'tcs_check': False,
            'email': 'john.doe@mail.com',
            'work_email': 'john.doe@nhs.co.uk',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'tcs_check': ['This field is required.']})

    def test_area_of_support_required(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'work_email': 'john.doe@nhs.co.uk',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'area_of_support': ['This field is required.']})

    def test_work_email_required(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
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
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'work_email': ['This field is required.']})

    def test_interview_experience_required(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'work_email': 'john.doe@nhs.co.uk',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'interview_experience': ['This field is required.']})

    def test_entrance_exam_experience_not_required(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'work_email': 'john.doe@nhs.co.uk',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertTrue(form.is_valid())

    def test_invalid_occupation(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'Doctor'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['occupation'],
                         ['Select a valid choice. Doctor is not one of the available choices.'])

    def test_missing_fields(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': '',
            'first_name': '',
            'last_name': '',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())

    def test_invalid_entrance_exam_experience(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UKCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['entrance_exam_experience'],
                         ['Select a valid choice. UKCAT is not one of the available choices.'])

    def test_invalid_interview_experience(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['Panel'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['interview_experience'],
                         ['Select a valid choice. Panel is not one of the available choices.'])

    def test_invalid_area_of_support(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['Personal Statement'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['area_of_support'],
                         ['Select a valid choice. Personal Statement is not one of the available choices.'])

    def test_invalid_sex(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'T',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sex'],
                         ['Select a valid choice. T is not one of the available choices.'])

    def test_invalid_hear_about_us(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'Word of Mouth',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['hear_about_us'],
                         ['Select a valid choice. Word of Mouth is not one of the available choices.'])

    def test_invalid_year_applied(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
            'email': 'john.doe@mail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'Y13',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'occupation': 'MD'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year_applied'],
                         ['Select a valid choice. Y13 is not one of the available choices.'])

    def test_labels(self):
        form = forms.MentorForm(data={
            'tcs_check': True,
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
        self.assertEqual(form.errors, {'name': ['This field is required.']})

    def test_education_level_required(self):
        form = forms.MentorQualificationForm(data={
            'name': 'Biology'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'education_level': ['This field is required.']})

    def test_invalid_education_level(self):
        form = forms.MentorQualificationForm(data={
            'name': 'Biology',
            'education_level': 'Y13'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['education_level'], ['Select a valid choice. Y13 is not one of the available '
                                                          'choices.'])


class AddMenteeFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertTrue(form.is_valid())

    def test_tcs_check_required(self):
        form = forms.MenteeForm(data={
            'tcs_check': False,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'tcs_check': ['This field is required.']})

    def test_missing_fields(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': '',
            'first_name': '',
            'last_name': '',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "",
            'mentor_help': "",
            'mentor_relationship': ""})
        self.assertFalse(form.is_valid())

    def test_invalid_sex(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'T',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sex'],
                         ['Select a valid choice. T is not one of the available choices.'])

    def test_invalid_year_applied(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'Y13',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year_applied'],
                         ['Select a valid choice. Y13 is not one of the available choices.'])

    def test_invalid_hear_about_us(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'Word of Mouth',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['hear_about_us'],
                         ['Select a valid choice. Word of Mouth is not one of the available choices.'])

    def test_invalid_entrance_exam_experience(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'M',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UKCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['entrance_exam_experience'],
                         ['Select a valid choice. UKCAT is not one of the available choices.'])

    def test_invalid_interview_experience(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'O',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['Panel'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['interview_experience'],
                         ['Select a valid choice. Panel is not one of the available choices.'])

    def test_invalid_area_of_support(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'O',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['Personal Statement'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['area_of_support'],
                         ['Select a valid choice. Personal Statement is not one of the available choices.'])

    def test_invalid_course(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'O',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'Medicine',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['course'],
                         ['Select a valid choice. Medicine is not one of the available choices.'])

    def test_invalid_current_application(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'O',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': None,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_application'],
                         ['This field is required.'])

    def test_labels(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'entrance_exam_experience': ['UCAT'],
            'interview_experience': ['P'],
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertIn('<label for="id_email">Email:</label>', form.as_p())
        self.assertIn('<label for="id_first_name">First name:</label>', form.as_p())
        self.assertIn('<label for="id_last_name">Last name:</label>', form.as_p())
        self.assertIn('<label for="id_sex">Sex:</label>', form.as_p())
        self.assertIn('<label for="id_year_applied">What is your current education level?</label>', form.as_p())
        self.assertIn('<label for="id_hear_about_us">How did you hear about us?</label>', form.as_p())
        self.assertIn('<label>What entrance exam experience have you had?</label>', form.as_p())
        self.assertIn('<label>What interview experience have you had?</label>', form.as_p())
        self.assertIn('<label>What do you need help with?</label>', form.as_p())
        self.assertIn('<label for="id_mentor_need">Why do you want a mentor and what do you hope to gain ?</label>',
                      form.as_p())
        self.assertIn('<label for="id_mentor_help">How will a mentor help with your application?</label>', form.as_p())
        self.assertIn('<label for="id_mentor_relationship">How will you go about fostering a good relationship your '
                      'mentor?</label>', form.as_p())
        self.assertIn('<label for="id_course">Course:</label>', form.as_p())
        self.assertIn('<label for="id_current_application">Are you applying this year?</label>', form.as_p())

    def test_non_required_fields(self):
        form = forms.MenteeForm(data={
            'tcs_check': True,
            'email': 'jane.doe@mail.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'sex': 'F',
            'year_applied': 'A2',
            'hear_about_us': 'WM',
            'area_of_support': ['PS'],
            'course': 'M',
            'current_application': True,
            'mentor_need': "I want a mentor because ...",
            'mentor_help': "Help me with ...",
            'mentor_relationship': "I will build a relationship by ..."})
        self.assertTrue(form.is_valid())


class AddMenteeQualificationFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2',
            'grade': 'A',
            'predicted': True})
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        form = forms.MenteeQualificationForm(data={
            'education_level': 'A2',
            'grade': 'A',
            'predicted': True})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['This field is required.']})

    def test_education_level_required(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'grade': 'A',
            'predicted': True})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'education_level': ['This field is required.']})

    def test_predicted_required(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2',
            'grade': 'A'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'predicted': ['This field is required.']})

    def test_grade_required(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2',
            'predicted': True})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'grade': ['This field is required.']})

    def test_invalid_education_level(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'Y13',
            'grade': 'A',
            'predicted': True})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['education_level'], ['Select a valid choice. Y13 is not one of the available '
                                                          'choices.'])

    def test_invalid_grade(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2',
            'grade': 'A+',
            'predicted': True})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['grade'], ['Select a valid choice. A+ is not one of the available '
                                                'choices.'])

    def test_invalid_predicted(self):
        form = forms.MenteeQualificationForm(data={
            'name': 'Biology',
            'education_level': 'A2',
            'grade': 'A',
            'predicted': None})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['predicted'], ['This field is required.'])
