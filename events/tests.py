from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event, UserProfile

class EventTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path='/path/to/chromedriver')  # Adjust path to your chromedriver
        cls.selenium.implicitly_wait(10)  # Implicit wait for elements

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username='testuser', password='password')
        self.event = Event.objects.create(title='Test Event', description='Test description', creator=self.user)
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_event_rsvp(self):
        self.selenium.get(self.live_server_url + reverse('event_detail', args=[self.event.id]))
        
        # Check if RSVP button is present and click it
        rsvp_button = self.selenium.find_element_by_id('rsvp-button')
        rsvp_button.click()

        # Assuming your app has a modal or confirmation message after RSVP, assert its presence
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'rsvp-confirmation'))
        )

        # Verify if RSVP was successful
        rsvp_confirmation = self.selenium.find_element_by_id('rsvp-confirmation')
        self.assertIn('You have RSVP\'d to this event', rsvp_confirmation.text)

    def test_event_filtering(self):
        self.selenium.get(self.live_server_url + reverse('event_list'))

        # Assuming you have a filter form with inputs for filtering events
        title_input = self.selenium.find_element_by_id('id_title')
        title_input.send_keys('Test Event')
        
        # Submit the form
        submit_button = self.selenium.find_element_by_xpath('//form[@id="filter-form"]/button[@type="submit"]')
        submit_button.click()

        # Verify if the filtered event appears in the list
        event_title = self.selenium.find_element_by_xpath('//div[@class="event-title"]')
        self.assertEqual(event_title.text, 'Test Event')

    def test_user_profile(self):
        self.selenium.get(self.live_server_url + reverse('user_profile'))

        # Assuming user profile details are displayed
        profile_title = self.selenium.find_element_by_tag_name('h2')
        self.assertEqual(profile_title.text, 'User Profile')

        # Check if user's username is displayed
        username_element = self.selenium.find_element_by_xpath('//span[@id="username"]')
        self.assertIn(self.user.username, username_element.text)

        # Check if collaborator status is displayed
        collaborator_status = self.selenium.find_element_by_xpath('//span[@id="collaborator-status"]')
        self.assertIn('Collaborator', collaborator_status.text)

    def test_navigation_authenticated_user(self):
        self.selenium.get(self.live_server_url)

        # Assuming user is logged in
        self.selenium.find_element_by_link_text('Logout').click()

        # Check if user is redirected to the login page after logout
        self.assertEqual(self.selenium.current_url, self.live_server_url + reverse('login'))

    def test_navigation_anonymous_user(self):
        self.selenium.get(self.live_server_url)

        # Check if 'Login' link is present and click it
        self.selenium.find_element_by_link_text('Login').click()

        # Check if user is redirected to the login page
        self.assertEqual(self.selenium.current_url, self.live_server_url + reverse('login'))

if __name__ == '__main__':
    import unittest
    unittest.main()
