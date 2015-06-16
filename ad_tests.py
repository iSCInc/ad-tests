"""Ad Eng selenium tests"""

import unittest
import logging
import sys
import os
import shutil
import dropbox
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import check_output


class TestAmazon(unittest.TestCase):
    """Test ads from Amazon provider"""

    send_dropbox = False

    @classmethod
    def setUpClass(self):
        self.logger = logging.getLogger('logger')
        self.url = 'http://adtest.wikia.com/wiki/SyntheticTests/Amazon'
        self.url_debug = self.url + '?amzn_debug_mode=1'
        self.amazon_script_url = 'amazon-adsystem.com/e/dtb'
        self.amazon_script_css = 'script[src*="' + self.amazon_script_url + '"]'
        self.amazon_iframe_css = 'iframe[src*="' + self.amazon_script_url + '"]'
        self.amazon_slot_css = 'div[id*=_gpt][data-gpt-slot-params*=amznslots]:not(.hidden)'
        self.amazon_gpt_params_pattern = '"amznslots":["a'
        self.timeout_seconds = 30
        self.log_folder = 'logs'
        # clear logs folder
        if os.path.exists(self.log_folder):
            shutil.rmtree(self.log_folder)
        os.makedirs(self.log_folder)

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def tearDown(self):
        if sys.exc_info()[0]:
            file_path = os.path.join(self.log_folder, self._testMethodName)
            img_file_path = file_path + '.png'
            html_file_path = file_path + '.html'
            self.driver.get_screenshot_as_file(img_file_path)
            with open(html_file_path, 'w') as f:
                f.write(self.driver.page_source.encode('utf-8'))
            if self.send_dropbox:
                key = 'TbN0tgnVu2oAAAAAAAAAD90u6_0IFv9kNEXnpD9c2inLh1Qwi-68-TyYMQsL6j48'
                self.client = dropbox.client.DropboxClient(key)
                self.client.put_file(img_file_path, open(img_file_path))
                self.client.put_file(html_file_path, open(html_file_path))
        self.driver.quit()

    def test_amazon_integration(self):
        """Test integration with Amazon provider"""
        self.driver.get(self.url)
        self.assertTrue(self.check_amazon_script_included())
        self.assertTrue(self.check_amazon_request_issued(False))

    def test_amazon_ads_success(self):
        """Test returned ads from Amazon provider"""
        self.driver.get(self.url_debug)
        self.assertTrue(self.check_amazon_script_included())
        self.assertTrue(self.check_amazon_request_issued(True))
        self.assertTrue(self.check_amazon_gpt_params())
        self.assertTrue(self.check_amazon_ad_present())

    def check_amazon_script_included(self):
        return self.check_element_by_css_selector(self.amazon_script_css)

    def check_amazon_request_issued(self, debug):
        url = self.url_debug if debug else self.url
        return self.check_request_issued(url, self.amazon_script_url)

    def check_amazon_gpt_params(self):
        amazon_slot = self.driver.find_element_by_css_selector(self.amazon_slot_css)
        data_gpt_slot_params = amazon_slot.get_attribute('data-gpt-slot-params')
        if self.amazon_gpt_params_pattern in data_gpt_slot_params:
            return True
        else:
            return False

    def check_amazon_ad_present(self):
        amazon_iframe = self.get_amazon_iframe(self.amazon_slot_css)
        self.driver.switch_to_frame(amazon_iframe)
        is_amazon_ad_present = self.check_element_by_css_selector(self.amazon_iframe_css)
        self.driver.switch_to_default_content()
        return is_amazon_ad_present

    def check_element_by_css_selector(self, css_selector):
        try:
            self.driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return True

    def check_request_issued(self, url, requested_url):
        out = check_output(['phantomjs', 'phantomjs/get_requested_urls.js', url])
        return True if requested_url in str(out) else False

    def wait_presence_of_element_located(self, css_selector):
        return WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    def get_amazon_iframe(self, amazon_slot_css):
        amazon_slot = self.wait_presence_of_element_located(self.amazon_slot_css)
        return amazon_slot.find_element_by_css_selector('div[id*=__container__] > iframe')


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('logger').setLevel(logging.DEBUG)
    if len(sys.argv) > 1 and sys.argv.pop() == 'send-dropbox':
        TestAmazon.send_dropbox = True
    unittest.main()
