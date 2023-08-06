'''
Created on 13 feb. 2018

@author: ex03210
'''

from nemonet.seleniumwebdriver.command_list import *

class Command(object):
    """
        All kind of selenium actions
    """

    def __init__(self, driver=None):
        """Constructor"""
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 60)

    def executeSequences(self, seq, g):

        for step in g.getSetup():
            self.execute_command(step.getAction())

        pa = seq.get()
        for l in pa:
            # logger.info("Execute sequence=%s" % (str(l)))
            for el in l:
                a = g.getVertex(el).getAction()
                self.execute_command(a)

    def execute_command(self, action : Action):
        """
        TODO : error handling
        :param action:
        :return:
        """
        command_type = action.getElementType()

        try:
            command_class = commands[command_type]
            if (command_class == None):
                pass  # Dummy Command for testing purposes
            else:
                c = command_class()
                c.execute(action, self.driver)
                return c

        except KeyError:
            # TODO : AssertionError is too generic, in need of an UnknownCommandException
            assert False, f"{command_type} is not a known command"


# TODO : this variable is exposed and needs a better location
commands = {
    'DUMMY': None,
    'CLICKABLE': ClickableCommand,
    'CLICKABLE_DOUBLE': ClickableDoubleCommand,
    'TEXTABLE': TextableCommand,
    'JSexec': JSexecCommand,
    'SELECTABLE': SelectableCommand,
    'OPENURL': OpenURLCommand,
    'SCREENSHOT': ScreenshotCommand,
    'CLEARTEXTABLE': ClearTextableCommand,
    'CLEARTEXTABLETAB': ClearTextableTabCommand,
    'TEXTABLE-ENTER': TextableEnterCommand,
    'COMPAREPNG': ComparePNGCommand,
    'COMPAREPNGPHASH': ComparePNGHashCommand,
    'WAIT': WaitCommand,
    'SCROLLTOP': ScrollTopCommand,
    'SCROLLBOTTOM': ScrollBottomCommand,
    'TAB': TabCommand,
    'CLICKABLE_RIGHT': ClickableRightCommand,
    'DRAG_AND_DROP': DragAndDropCommand,
    'GOTO_FRAME': GoToFrameCommand,
    'SAVE_CURRENT_URL': SaveCurrentURLCommand,
    'SPLIT_STORED_URL': SplitStoredURLCommand,
    'FORMAT_STRINGS': FormatStringsCommand,
    'STORE_STRING': StoreStringCommand,
    'SITE_SETTINGS': SiteSettingsCommand,
    'TABS_AND_ENTER': TabsAndEnterCommand,
    'TABS_AND_TEXT': TabsAndTextCommand,
    'BROWSER_TABS_ADD': BrowserTabsAddCommand,
    'BROWSER_TABS_GOTO': BrowserTabsGoToCommand,
    'LOG_CURRENT_URL': LogCurrentURLCommand,
    'OPEN_STORED_URL': OpenStoredURLCommand,
    'BROWSER_TABS_GOTO_CURRENT': BrowserTabsGoToCurrentCommand,
    'TEXT_CURRENT_POSITION': TextCurrentPositionCommand,
    'TEXT_CURRENT_POSITION_STAMP': TextCurrentPositionStampCommand,
    'DRAG_AND_DROP_MOUSE': DragAndDropMouseCommand,
    'DRAG_AND_DROP_WITH_OFFSET': DragAndDropWithOffsetCommand,
    'SWITCH_TO_ALERT_AND_CONFIRM': SwitchToAlertAndConfirmCommand,
    'REMOVE_HTML_ELEMENT': RemoveHTMLElementCommand,
    'SPLIT_URL_AND_STORE': SplitURLAndStoreCommand,
    'SELECT_FROM_DROP_DOWN': SelectFromDropDownCommand
}
