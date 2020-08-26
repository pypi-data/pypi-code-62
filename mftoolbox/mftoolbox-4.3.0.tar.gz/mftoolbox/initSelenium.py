from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
# noinspection SpellCheckingInspection

options = webdriver.ChromeOptions()

chrome_preferences = {'profile.managed_default_content_settings.images': 2}
options.add_argument("headless")
# noinspection SpellCheckingInspection
options.add_experimental_option("prefs", chrome_preferences)
browser = webdriver.Chrome(options=options, service_args=['--silent'], desired_capabilities=caps)