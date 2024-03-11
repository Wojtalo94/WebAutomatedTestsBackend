from tools.AppLogAnalyzer import AppLogAnalyzer
from tools.AppController import AppController
from behave import fixture
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from tools.config import FULLSCREEN, INCOGNITO, BASE_URL, APP_LOGS

def set_focus_on_browser(driver):
    action = ActionChains(driver)
    window_size = driver.get_window_rect()
    x_coordinate = window_size['width'] / 2
    y_coordinate = window_size['height'] / 2
    action.move_by_offset(x_coordinate, y_coordinate)
    action.click()
    action.perform()

@fixture
def run_browser(context):
    if context.browser == "chrome":
        options = webdriver.ChromeOptions()
        if FULLSCREEN:
            options.add_argument("--start-maximized")
        if INCOGNITO:
            options.add_argument("--incognito")
        if APP_LOGS:
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        context.driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=options)

    elif context.browser == "firefox":
        context.driver = webdriver.Firefox(service=webdriver.FirefoxService(GeckoDriverManager().install()))
        if FULLSCREEN:
            context.driver.maximize_window()

    elif context.browser == "edge":
        context.driver = webdriver.Edge(service=webdriver.EdgeService(EdgeChromiumDriverManager().install()))
        if FULLSCREEN:
            context.driver.maximize_window()

    else:
        raise ValueError("Unsupported browser: " + context.browser)

    context.driver.get(BASE_URL)
    #context.AppLogAnalyzer = AppLogAnalyzer(context.driver)
    context.AppController = AppController(context.driver)

    yield

    context.driver.close()