#!/usr/bin/env python3

from os import path
from logging import basicConfig, getLogger, StreamHandler, Formatter
from socket import gethostname
from datetime import datetime
from unittest import TestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


PRJ_ROOT_PATH = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..'))
chromedriver = path.join(PRJ_ROOT_PATH, 'deployment', 'chromedriver')
RESULTS_PATH = path.join(PRJ_ROOT_PATH, 'e2e_tests')
LOGFILE = path.join(RESULTS_PATH, 'log_.log')
SCREENSHOT_PATH = RESULTS_PATH


class BaseTestCase(TestCase):
    current_result = None  # holds last result object passed to run method

    def run(self, result=None):
        self.current_result = result  # remember result for use in tearDown
        TestCase.run(self, result)  # call superclass run method

    @classmethod
    def logging_setup(cls, log_level='INFO'):
        lformat = '%(asctime)s;%(filename)s;%(funcName)s()\t%(levelname)s\t%(message)s'
        basicConfig(level=log_level,
                    format=lformat,
                    filename=LOGFILE,
                    filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = StreamHandler()
        console.setFormatter(Formatter(lformat))
        console.setLevel(log_level)
        # # tell the handler to use the same format as the log file
        # console.setFormatter('%(levelname)s\t%(message)s')
        # add the handler to the root logger
        getLogger('').addHandler(console)

    def setUp(self):
        self.addCleanup(self.clean_up)
        self.logging_setup()
        self.logger = getLogger()
        self.db_connection = None

        self.browser = webdriver.Chrome(chromedriver)
        self.browser.set_window_size(1366, 768)

    def clean_up(self):
        """Hook method which a test project shall override.
        If setUp() fails, meaning that tearDown() is not called, then any cleanup functions added will still be called.
        """
        pass

    def tearDown(self):
        try:
            self.browser.close()
        except WebDriverException:
            # Fail gracefully if the browser is no longer reachable
            self.logger.debug('did not close browser window')
        else:
            self.logger.debug('browser closed...')

    def take_screenshot(self, identifier):
        """Take a screenshot and write it to the result folder as a png file.
        The naming convention is:
        machinename_datetimestamp_identifier.png
        :param str identifier: A string to identify the filename of a screenshot.
        """
        file_name = path.join(SCREENSHOT_PATH, '{}_{}_{}.png'.format(
                              gethostname(),
                              datetime.now().strftime('%Y%m%d%H%M%S%f'),
                              identifier))
        self.browser.save_screenshot(file_name)
        self.logger.info('screenshot made: {}'.format(file_name))


class BasicRegressionTests(BaseTestCase):

    def test_header_footer_present(self):
        self.browser.get('http://localhost:8000')
        self.take_screenshot('homepage')
        self.check_html_title('_kg')
        self.check_header_block()
        self.check_content_block()
        self.check_footer_block()

    def check_html_title(self, title):
        self.logger.info('expected html title: {}'.format(title))
        assert title == self.browser.title, \
            'check title\nexpected: {}\nobserved: {}'.format(title, self.browser.title)

    def check_header_block(self):
        # TODO: 'validate that the header block is present.'
        # TODO: 'validate that the header block has the top image, and 4 buttons.'
        pass

    def check_content_block(self):
        # TODO: 'validate that the page-specific content block is present.'
        pass

    def check_footer_block(self):
        # TODO: 'validate that the footer block is present.'
        # TODO: 'Nice-to-have: validate that the social media sharing buttons work'
        pass
