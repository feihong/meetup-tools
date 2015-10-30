import os
import os.path as op
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


browser = None


class MemberRemover(object):
    def __init__(self, short_name, explanation_template, explanation_dict):
        global browser

        self.base_url = 'http://www.meetup.com/%s' % short_name
        self.explanation_template = explanation_template
        self.explanation_dict = explanation_dict

        profile = get_profile()
        browser = webdriver.Firefox(firefox_profile=profile)

    def remove(self, member):
        member_id = member['Member ID']
        browser.get('%s/members/remove/?id=%s' % (self.base_url, member_id))
        if 'Sorry, an error occurred' in browser.page_source:
            return

        print('Sleeping for %d seconds to simulate human laziness' % random.randint(5, 10))
        time.sleep(seconds)

        textarea = browser.find_element_by_css_selector('textarea[name=emailBlurb]')
        textarea.send_keys(self.explanation % member)

        checkbox = browser.find_element_by_css_selector('input[name=ccOrg]')
        checkbox.click()

        button = browser.find_element_by_css_selector('input[type=submit]')
        button.click()


def get_profile():
    profile_dir = op.expanduser('~/Library/Application Support/Firefox/Profiles'
    for profile in os.listdir(profile_dir):
        if 'meetup' in profile:
            profile_path = op.join(profile_dir, profile)
            return FirefoxProfile(profile_path)

    return None
