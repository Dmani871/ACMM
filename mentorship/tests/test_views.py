from django.test import TestCase
from django.urls import reverse


class ApplicationsViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/mentorship/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mentorship:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mentorship:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentorship/applications.html')


class ThankYouViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/mentorship/thanks')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mentorship:thank_you"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mentorship:thank_you"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentorship/thank_you.html')


class NextYearViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/mentorship/next_year')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mentorship:next_year"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mentorship:next_year"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentorship/next_year.html')


class MentorViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/mentorship/mentor/signup')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mentorship:mentor"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mentorship:mentor"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentorship/mentor_signup.html')


class MenteeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/mentorship/mentee/signup')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mentorship:mentee"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mentorship:mentee"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentorship/mentee_signup.html')
# TODO:Selenium test
