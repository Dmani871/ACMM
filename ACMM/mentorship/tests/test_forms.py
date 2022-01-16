import unittest
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

class TestMentorSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    
    def test_mentor_signup_fire(self):
        self.driver.get("http://127.0.0.1:8000/mentorship/mentor/signup")
        self.driver.find_element_by_id('id_first_name').send_keys("John")
        self.driver.find_element_by_id('id_last_name').send_keys("Doe")
        self.driver.find_element_by_id('id_email').send_keys("john.doe@example.com")
        sex_select = Select(self.driver.find_element_by_id('id_sex'))
        sex_select.select_by_visible_text('M')
        occupation_select = Select(self.driver.find_element_by_id('id_occupation'))
        occupation_select.select_by_visible_text('Doctor')
        year_applied_select = Select(self.driver.find_element_by_id('id_year_applied'))
        year_applied_select.select_by_visible_text('Graduate')
        self.driver.find_element_by_xpath("//input[@name='entrance_exam_experience']").click()
        self.driver.find_element_by_xpath("//input[@name='interview_experience']").click()
        self.driver.find_element_by_xpath("//input[@name='area_of_support']").click()
        self.driver.find_element_by_id('id_mentorqualification_set-0-name').send_keys("Mathematics")
        q1_select = Select(self.driver.find_element_by_id('id_mentorqualification_set-0-education_level'))
        q1_select.select_by_visible_text('A Level')
        self.driver.find_element_by_id('id_mentorqualification_set-1-name').send_keys("Biology")
        q2_select = Select(self.driver.find_element_by_id('id_mentorqualification_set-1-education_level'))
        q2_select.select_by_visible_text('A Level')
        self.driver.find_element_by_id('id_mentorqualification_set-2-name').send_keys("Psychology")
        q3_select = Select(self.driver.find_element_by_id('id_mentorqualification_set-2-education_level'))
        q3_select.select_by_visible_text('A Level')
        self.driver.find_element_by_id('signup').click()
        self.assertIn("http://127.0.0.1:8000/mentorship/thanks", self.driver.current_url)

    
    def tearDown(self):
        self.driver.quit


class TestMenteeSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    
    def test_mentee_signup_fire(self):
        self.driver.get("http://127.0.0.1:8000/mentorship/mentee/signup")
        self.driver.find_element_by_id('id_first_name').send_keys("John")
        self.driver.find_element_by_id('id_last_name').send_keys("Doe")
        self.driver.find_element_by_id('id_email').send_keys("john.doe@example.com")
        sex_select = Select(self.driver.find_element_by_id('id_sex'))
        sex_select.select_by_visible_text('M')
        course_select = Select(self.driver.find_element_by_id('id_course'))
        course_select.select_by_visible_text('Medicine')
        year_applied_select = Select(self.driver.find_element_by_id('id_year_applied'))
        year_applied_select.select_by_visible_text('Graduate')
        self.driver.find_element_by_xpath("//input[@name='entrance_exam_experience']").click()
        self.driver.find_element_by_xpath("//input[@name='interview_experience']").click()
        self.driver.find_element_by_xpath("//input[@name='area_of_support']").click()
        self.driver.find_element_by_id('id_mentor_need').send_keys("Mentor need")
        self.driver.find_element_by_id('id_mentor_help').send_keys("Mentor help")
        self.driver.find_element_by_id('id_mentor_relationship').send_keys("Mentor relationship")
        self.driver.find_element_by_id('id_menteequalification_set-0-name').send_keys("Mathematics")
        q1_education_select = Select(self.driver.find_element_by_id('id_menteequalification_set-0-education_level'))
        q1_education_select.select_by_visible_text('A Level')
        q1_grade_select = Select(self.driver.find_element_by_id('id_menteequalification_set-0-grade'))
        q1_grade_select.select_by_visible_text('A')
        self.driver.find_element_by_id('id_menteequalification_set-1-name').send_keys("Biology")
        q2_select = Select(self.driver.find_element_by_id('id_menteequalification_set-1-education_level'))
        q2_select.select_by_visible_text('A Level')
        q2_grade_select = Select(self.driver.find_element_by_id('id_menteequalification_set-1-grade'))
        q2_grade_select.select_by_visible_text('A')
        self.driver.find_element_by_id('id_menteequalification_set-2-name').send_keys("Psychology")
        q3_select = Select(self.driver.find_element_by_id('id_menteequalification_set-2-education_level'))
        q3_select.select_by_visible_text('A Level')
        q3_grade_select = Select(self.driver.find_element_by_id('id_menteequalification_set-2-grade'))
        q3_grade_select.select_by_visible_text('A')
        self.driver.find_element_by_id('signup').click()
        self.assertIn("http://127.0.0.1:8000/mentorship/thanks", self.driver.current_url)

    def tearDown(self):
        self.driver.quit


if __name__ == '__main__':
    unittest.main()


