from django.test import TestCase

from mentorship import forms

VALID_MENTOR_FORM = {
    "tcs_check": True,
    "email": "john.doe@mail.com",
    "contact_consent": "Y",
    "number": "01",
    "first_name": "John",
    "last_name": "Doe",
    "year_applied": "A2",
    "hear_about_us": "WM",
    "entrance_exam_experience": ["UCAT"],
    "interview_experience": ["P"],
    "area_of_support": ["PS"],
    "occupation": "MD",
    "additional_info": "I am excited to apply",
}

VALID_MENTEE_FORM = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@mail.com",
    "number": "01",
    "contact_consent": "Y",
    "year_applied": "A2",
    "course": "M",
    "current_application": True,
    "wp_scheme": True,
    "family_support": True,
    "applied_before": True,
    "state_educated": True,
    "commitment": True,
    "entrance_exam_experience": ["UCAT"],
    "interview_experience": ["P"],
    "area_of_support": ["PS"],
    "mentor_need": "I want a mentor because ...",
    "mentor_help": "Help me with ...",
    "mentor_relationship": "I will build a relationship by ...",
    "hear_about_us": "WM",
    "tcs_check": True,
}


class AddMentorFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MentorForm(data=VALID_MENTOR_FORM)
        self.assertTrue(form.is_valid())

    def _required(self, field):
        invalid_form = {**VALID_MENTOR_FORM}
        del invalid_form[field]
        form = forms.MentorForm(data=invalid_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(dict(form.errors), {field: ["This field is required."]})

    def _invalid(self, field, is_list=False):
        if is_list:
            value = ["Panel"]
            err_msg = (
                "Select a valid choice. Panel is not one of the available choices."
            )
        else:
            value = "Panel"
            err_msg = (
                "Select a valid choice. Panel is not one of the available choices."
            )

        invalid_from = {**VALID_MENTOR_FORM, field: value}
        form = forms.MentorForm(data=invalid_from)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[field], [err_msg])

    def test_email_required(self):
        self._required("email")

    def test_first_name_required(self):
        self._required("first_name")

    def test_last_name_required(self):
        self._required("last_name")

    def test_number_required(self):
        self._required("number")

    def test_contact_consent_required(self):
        self._required("contact_consent")

    def test_occupation_required(self):
        self._required("occupation")

    def test_invalid_occupation_errors(self):
        self._invalid("occupation", is_list=False)

    def test_year_applied_required(self):
        self._required("year_applied")

    def test_invalid_year_applied_errors(self):
        self._invalid("year_applied", is_list=False)

    def test_entrance_exam_experience_not_required(self):
        form = {**VALID_MENTOR_FORM}
        del form["entrance_exam_experience"]
        form = forms.MentorForm(data=form)
        self.assertTrue(form.is_valid())

    def test_invalid_entrance_exam_experience(self):
        self._invalid("entrance_exam_experience", is_list=True)

    def test_interview_experience_required(self):
        self._required("interview_experience")

    def test_invalid_interview_experience(self):
        self._invalid("interview_experience", is_list=True)

    def test_area_of_support_required(self):
        self._required("area_of_support")

    def test_invalid_area_of_support_experience(self):
        self._invalid("area_of_support", is_list=True)

    def test_hear_about_us_required(self):
        self._required("hear_about_us")

    def test_invalid_hear_about_us(self):
        self._invalid("hear_about_us")

    def test_tcs_check_required(self):
        self._required("tcs_check")

    def test_tcs_checked(self):
        invalid_from = {**VALID_MENTOR_FORM, "tcs_check": False}
        form = forms.MentorForm(invalid_from)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"tcs_check": ["This field is required."]})

    def test_missing_fields(self):
        invalid_from = {**VALID_MENTOR_FORM}
        del invalid_from["first_name"]
        del invalid_from["year_applied"]
        form = forms.MentorForm(invalid_from)
        self.assertFalse(form.is_valid())

    def test_labels(self):
        form = forms.MentorForm(data=VALID_MENTOR_FORM)
        # Personal Information
        self.assertIn('<label for="id_email">Email:</label>', form.as_p())
        self.assertIn('<label for="id_first_name">First name:</label>', form.as_p())
        self.assertIn('<label for="id_last_name">Last name:</label>', form.as_p())
        self.assertIn('<label for="id_number">Contact Number:</label>', form.as_p())
        self.assertIn(
            '<label for="id_contact_consent">Would you be happy to be added to the WhatsApp Broadcast group where you will receive key information on the mentoring scheme?</label>',
            form.as_p(),
        )
        # Background Information
        self.assertIn('<label for="id_occupation">Occupation:</label>', form.as_p())
        self.assertIn(
            '<label for="id_year_applied">Qualification level prior to studying Medicine/Dentistry:</label>',
            form.as_p(),
        )
        self.assertIn("<label>What exam experience do you have?</label>", form.as_p())
        self.assertIn(
            "<label>What interview experience do you have?</label>", form.as_p()
        )
        self.assertIn(
            "<label>What area can you provide support in?</label>", form.as_p()
        )
        self.assertIn('<label for="id_occupation">Occupation:</label>', form.as_p())
        self.assertIn(
            '<label for="id_hear_about_us">How did you hear about us?</label>',
            form.as_p(),
        )
        self.assertIn(
            '<label for="id_additional_info">Any additional comments?</label>',
            form.as_p(),
        )


class AddMenteeFormTests(TestCase):
    def _required(self, field):
        invalid_form = {**VALID_MENTEE_FORM}
        del invalid_form[field]
        form = forms.MenteeForm(data=invalid_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(dict(form.errors), {field: ["This field is required."]})

    def _invalid(self, field, is_list=False):
        if is_list:
            value = ["Panel"]
            err_msg = (
                "Select a valid choice. Panel is not one of the available choices."
            )
        else:
            value = "Panel"
            err_msg = (
                "Select a valid choice. Panel is not one of the available choices."
            )

        invalid_from = {**VALID_MENTEE_FORM, field: value}
        form = forms.MenteeForm(data=invalid_from)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[field], [err_msg])

    def test_valid_form(self):
        form = forms.MenteeForm(data=VALID_MENTEE_FORM)
        self.assertTrue(form.is_valid())

    def test_email_required(self):
        self._required("email")

    def test_first_name_required(self):
        self._required("first_name")

    def test_last_name_required(self):
        self._required("last_name")

    def test_number_required(self):
        self._required("number")

    def test_contact_consent_required(self):
        self._required("contact_consent")

    def test_course_required(self):
        self._required("course")

    def test_invalid_course_errors(self):
        self._invalid("course", is_list=False)

    def test_year_applied_required(self):
        self._required("year_applied")

    def test_invalid_year_applied_errors(self):
        self._invalid("year_applied", is_list=False)

    def test_applied_before_required(self):
        self._required("applied_before")

    def test_invalid_applied_before_errors(self):
        self._invalid("applied_before", is_list=False)

    def test_state_educated_required(self):
        self._required("state_educated")

    def test_invalid_state_educated_errors(self):
        self._invalid("state_educated", is_list=False)

    def test_family_support_required(self):
        self._required("family_support")

    def test_invalid_family_support_errors(self):
        self._invalid("family_support", is_list=False)

    def test_commitment_required(self):
        self._required("commitment")

    def test_invalid_commitment_errors(self):
        self._invalid("commitment", is_list=False)

    def test_wp_scheme_required(self):
        self._required("wp_scheme")

    def test_invalid_wp_scheme_errors(self):
        self._invalid("wp_scheme", is_list=False)

    def test_entrance_exam_experience_not_required(self):
        form = {**VALID_MENTEE_FORM}
        del form["entrance_exam_experience"]
        form = forms.MenteeForm(data=form)
        self.assertTrue(form.is_valid())

    def test_invalid_entrance_exam_experience(self):
        self._invalid("entrance_exam_experience", is_list=True)

    def test_invalid_interview_experience(self):
        self._invalid("interview_experience", is_list=True)

    def test_area_of_support_required(self):
        self._required("area_of_support")

    def test_invalid_area_of_support_experience(self):
        self._invalid("area_of_support", is_list=True)

    def test_hear_about_us_required(self):
        self._required("hear_about_us")

    def test_invalid_hear_about_us(self):
        self._invalid("hear_about_us")

    def test_tcs_check_required(self):
        self._required("tcs_check")

    def test_tcs_checked(self):
        invalid_from = {**VALID_MENTEE_FORM, "tcs_check": False}
        form = forms.MenteeForm(invalid_from)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"tcs_check": ["This field is required."]})

    def test_missing_fields(self):
        invalid_from = {**VALID_MENTEE_FORM}
        del invalid_from["first_name"]
        del invalid_from["year_applied"]
        form = forms.MenteeForm(invalid_from)
        self.assertFalse(form.is_valid())

    def test_labels(self):
        form = forms.MenteeForm(data=VALID_MENTEE_FORM)
        # Personal Information
        self.assertIn('<label for="id_email">Email:</label>', form.as_p())
        self.assertIn('<label for="id_first_name">First name:</label>', form.as_p())
        self.assertIn('<label for="id_last_name">Last name:</label>', form.as_p())
        self.assertIn('<label for="id_number">Contact Number:</label>', form.as_p())
        self.assertIn(
            '<label for="id_contact_consent">Would you be happy to be added to the WhatsApp Broadcast group where you will receive key information on the mentoring scheme?</label>',
            form.as_p(),
        )
        # Background information
        self.assertIn(
            '<label for="id_year_applied">What is your current education level?</label>',
            form.as_p(),
        )
        self.assertIn(
            '<label for="id_hear_about_us">How did you hear about us?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_hear_about_us">How did you hear about us?</label>',
            form.as_p(),
        )
        self.assertIn(
            '<label for="id_hear_about_us">How did you hear about us?</label>',
            form.as_p(),
        )
        self.assertIn(
            "<label>What entrance exam experience have you had?</label>", form.as_p()
        )
        self.assertIn(
            "<label>What interview experience have you had?</label>", form.as_p()
        )
        self.assertIn("<label>What do you need help with?</label>", form.as_p())
        self.assertIn(
            '<label for="id_mentor_need">Why do you want a mentor and what do you hope to gain ?</label>',
            form.as_p(),
        )
        self.assertIn(
            '<label for="id_mentor_help">How will a mentor help with your application?</label>',
            form.as_p(),
        )
        self.assertIn(
            '<label for="id_mentor_relationship">How will you go about fostering a good relationship your '
            "mentor?</label>",
            form.as_p(),
        )
        self.assertIn('<label for="id_course">Course:</label>', form.as_p())
        self.assertIn(
            '<label for="id_current_application">Are you applying this year?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_commitment">Are you able to commit to monthly meetings with your mentor throughout the year of the mentoring programme?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_state_educated">Do you attend a state school?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_family_support">Do you have a parent(s) who are doctors?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_applied_before">Have you applied before?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_wp_scheme">Are you applying via a widening participation (WP) scheme?</label>',
            form.as_p(),
        )

        self.assertIn(
            '<label for="id_tcs_check">I have read and agree to the <a href="/mentorship/privacy">Privacy Policy</a> :</label>',
            form.as_p(),
        )


class AddMenteeQualificationFormTests(TestCase):
    def test_valid_form(self):
        form = forms.MenteeQualificationForm(
            data={
                "name": "Biology",
                "education_level": "A2",
                "grade": "A",
                "predicted": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        form = forms.MenteeQualificationForm(
            data={"education_level": "A2", "grade": "A", "predicted": True}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"name": ["This field is required."]})

    def test_education_level_required(self):
        form = forms.MenteeQualificationForm(
            data={"name": "Biology", "grade": "A", "predicted": True}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"education_level": ["This field is required."]})

    def test_predicted_required(self):
        form = forms.MenteeQualificationForm(
            data={"name": "Biology", "education_level": "A2", "grade": "A"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"predicted": ["This field is required."]})

    def test_grade_required(self):
        form = forms.MenteeQualificationForm(
            data={"name": "Biology", "education_level": "A2", "predicted": True}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"grade": ["This field is required."]})

    def test_invalid_education_level(self):
        form = forms.MenteeQualificationForm(
            data={
                "name": "Biology",
                "education_level": "Y13",
                "grade": "A",
                "predicted": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["education_level"],
            ["Select a valid choice. Y13 is not one of the available " "choices."],
        )

    def test_invalid_grade(self):
        form = forms.MenteeQualificationForm(
            data={
                "name": "Biology",
                "education_level": "A2",
                "grade": "A+",
                "predicted": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["grade"],
            ["Select a valid choice. A+ is not one of the available " "choices."],
        )

    def test_invalid_predicted(self):
        form = forms.MenteeQualificationForm(
            data={
                "name": "Biology",
                "education_level": "A2",
                "grade": "A",
                "predicted": None,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["predicted"], ["This field is required."])
