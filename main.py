from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep

from credentials import email
from credentials import password
from credentials import chromedriver_path
from credentials import chrome_profile_path

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=720x480")
    options.add_argument("--use-fake-ui-for-media-stream")
    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_setting_values.geolocation": 1 
    })
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    return driver

def login_if_needed(driver):
    google_button_list = driver.find_elements_by_xpath("//*[text()='Logga in med Google']")
    if (len(google_button_list) > 0):
        google_button_list[0].click()
        driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
        sleep(2)

        email_field = driver.find_element_by_css_selector("input[type='email']")
        email_field.send_keys(email)
        email_field.send_keys(Keys.ENTER)
        sleep(2)

        password_field = driver.find_element_by_css_selector("input[type='password']")
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        sleep(2)
    else:
        print('Already logged in :)')

def allow_location_if_needed(driver):
    allow_button_list = driver.find_elements_by_xpath("//*[text()='Tillåt']")
    if (len(allow_button_list) > 0):
        allow_button_list[0].click()
    else:
        print('Location services already allowed :)')

def activate_notifications_if_needed(driver):
    allow_button_list = driver.find_elements_by_xpath("//*[text()='Aktivera']")
    if (len(allow_button_list) > 0):
        allow_button_list[0].click()
    else:
        print('Notifications already activated :)')

def allow_popups_if_needed(driver):
    # two alerts are expected - notifications and location data
    for _ in range(2):
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to_alert().accept()
        except TimeoutException:
            print("Couldn't find first alert, moving on...")

def perform_swiping(driver, swipe_count):
    for _ in range(swipe_count):
        sleep(2)
        driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)


def main():
    driver = setup_driver()
    driver.get("https:tinder.com")
    sleep(2)

    login_if_needed(driver)
    allow_location_if_needed(driver)
    activate_notifications_if_needed(driver)

    perform_swiping(driver=driver, swipe_count=100)

    print("Finished")

if __name__ == "__main__":
    main()    
