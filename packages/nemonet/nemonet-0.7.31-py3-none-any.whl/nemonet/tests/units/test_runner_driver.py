import unittest
from nemonet.runner.webdriver import ChromeTestDriver

class RunnerDriverTestCase(unittest.TestCase):

    def test_chrometestdriver_config_init(self):

        """ tests if ChromeTestDrivers can be correctly instantiated
            with a specific configuration """

        flag = ["dummy"]
        config = {
            "headless" : True,
            "experimental_flags" : flag
        }

        c = ChromeTestDriver(config=config)

        msg = "ChromeTestDriver init with configuration issue for :"
        self.assertTrue(c.headless, msg=msg + "headless")
        self.assertEqual(c.experimental_flags, flag, msg=msg + "experimental flags")