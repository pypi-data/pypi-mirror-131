from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestDriver:

    def open(self):
        pass

    def quit(self):
        pass


class ChromeTestDriver(TestDriver):

    @classmethod
    @property
    def default_config(cls) -> dict:
        return {
            "headless": False,
            "experimental_flags": None
        }

    def __init__(self, config=None):

        if not config:
            config = self.default_config

        self._experimental_flags = config["experimental_flags"]
        self._headless = config["headless"]
        self._driver = None

    @property
    def experimental_flags(self) -> list:
        ef = self._experimental_flags
        if ef:
            return ef.copy()
        else :
            return []

    @property
    def headless(self) -> bool:
        return self._headless

    @property
    def options(self) -> Options:
        """ returns an instance of ChromeOptions based on current configuration """
        options = Options()
        if self.experimental_flags:
            chrome_local_state_prefs = {'browser.enabled_labs_experiments': self.experimental_flags}
            options.add_experimental_option('localState', chrome_local_state_prefs)
        if self.headless:
            options.add_argument("--headless")
        return options

    def open(self):
        self._driver = webdriver.Chrome(options=self.options)
        self._driver.maximize_window()

    def quit(self):
        self._driver.quit()

    def get_native_driver(self) -> webdriver.Chrome:
        return self._driver
