from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages import AviasalesSearchPage, AviasalesResultsPage, BookingPage

def before_scenario(context, scenario):
    # Запускаем браузер перед каждым сценарием
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    context.driver.maximize_window()
    context.driver.implicitly_wait(10)

    # Инициализируем твои Page Objects
    context.search_page = AviasalesSearchPage(context.driver)
    context.results_page = AviasalesResultsPage(context.driver)
    context.booking_page = BookingPage(context.driver)

def after_scenario(context, scenario):
    context.driver.quit()