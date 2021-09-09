from selenium import webdriver


class RemoteDriver(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                             f'(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
        options.add_argument('--mute-audio')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.options = options

    def set_driver(self, headless=True, write_log=False):
        self.options.headless = headless
        log_files = None
        if write_log:
            log_files = ["--verbose", "--log-path=chromedriver.log"]
        return webdriver.Chrome(
            options=self.options,
            executable_path='chromedriver.exe',
            service_args=log_files
        )
