import os

from selenium import webdriver

from app.remote.errorhandler import err_catch, log


class RemoteDriver(object):
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        try:
            profile = 'firefox_profile'
            self.fp = webdriver.FirefoxProfile(profile)
        except Exception as e:
            log.error(err_catch(e))
            log.error('Tolong Copy firefox_profile')
            self.fp = webdriver.FirefoxProfile()

    def set_driver(self, headless=True, write_log=False, accept_insecure_cert=False):
        self.options.headless = headless
        self.options.accept_insecure_certs = accept_insecure_cert
        if write_log:
            log_files = 'geckodriver.log'
        else:
            log_files = os.devnull
        return webdriver.Firefox(
            options=self.options,
            executable_path='geckodriver.exe',
            service_log_path=log_files,
            firefox_profile=self.fp
        )
