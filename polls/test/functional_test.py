import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from polls.models import Question, Choice
from django.utils import timezone
from django.contrib.auth.models import User


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(choice_text, question):
    return Choice.objects.create(choice_text=choice_text, question=question)


def question_for_test():
    question = create_question("What's your favorite color?", days=-1)
    return question


class FunctionalTestCase(LiveServerTestCase):
    username = "username"
    password = "password"

    def setUp(self):
        """This method is called before every test."""
        self.browser = webdriver.Chrome(executable_path=r'C:\Users\User\Desktop\Driver\chromedriver.exe')
        super(FunctionalTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTestCase, self).tearDown()

    def get_index_url(self):
        self.browser.get(self.live_server_url + '/polls/')

    def find_tag_name_a(self):
        links = self.browser.find_elements_by_tag_name('a')
        return links

    def test_header(self):
        self.get_index_url()
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Polls list', header.text)

    def test_is_question_exist(self):
        question = question_for_test()
        self.get_index_url()
        question_id = self.browser.find_element_by_id(f"{question.id}")
        self.assertEqual(question_id.text, "What's your favorite color?")

    def test_question_detail(self):
        question = question_for_test()
        self.get_index_url()
        links = self.find_tag_name_a()
        links[1].click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/polls/' + f"{question.id}/")

    def test_question_result(self):
        question = question_for_test()
        choice = create_choice("Red", question)
        User.objects.create_user(self.username, password=self.password)
        self.browser.get(self.live_server_url + '/accounts/login')
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("login").click()
        link = self.find_tag_name_a()
        link[0].click()
        choice1 = self.browser.find_element_by_id(f"choice{choice.id}")
        choice1.click()
        self.browser.find_element_by_id(f"vote").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/polls/' + f"{question.id}/results/")
