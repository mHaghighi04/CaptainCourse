from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriver path
PATH = "/usr/local/bin/chromedriver"
service = Service(PATH)
driver = webdriver.Chrome(service=service)

# Open the RateMyProfessors UCSB page
url = "https://www.ratemyprofessors.com/search/professors/1077?q=*"
driver.get(url)

try:
   # Wait for the school search bar to load and input "University of California Santa Barbara"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Your school']"))
    )
    school_search_bar = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Your school']")
    school_name = "University of California Santa Barbara"
    school_search_bar.send_keys(school_name)
    school_search_bar.send_keys(Keys.RETURN)

    # # Wait for the first search result and click it
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "TeacherSchoolSelectorInput__SelectedSchoolTextName-npx66c-2"))
    # )
    # school_button = driver.find_element(By.CLASS_NAME, "TeacherSchoolSelectorInput__SelectedSchoolTextName-npx66c-2")
    # school_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.SchoolCard__StyledSchoolCard-sc-130cnkk-0.bJboOI"))
    )
    school_card = driver.find_element(By.CSS_SELECTOR, "a.SchoolCard__StyledSchoolCard-sc-130cnkk-0.bJboOI")
    school_card.click()

      # Wait for the professor search bar to load and input professor name "Ziad Matni"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Professor name']"))
    )
    professor_search_bar = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Professor name']")
    professor_name = "Ziad Matni"
    professor_search_bar.send_keys(professor_name)
    professor_search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2"))
    )

    # Extract the score for the professor
    professor_score = driver.find_element(By.CLASS_NAME, "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2").text

    print(f"School: {school_name}")
    print(f"Professor: {professor_name}")
    print(f"Score: {professor_score}")

    time.sleep(5)

    # # Wait for the search results to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "TeacherCard__InfoRatingWrapper-syjs0d-3 kcbPEB"))
    # )

    # # Click the first search result
    # first_result = driver.find_element(By.CLASS_NAME, "TeacherCard__InfoRatingWrapper-syjs0d-3 kcbPEB")
    # first_result.click()

    # # Wait for the professor's rating page to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "RatingValue__Numerator-qw8sqy-2 liyUjw"))
    # )

    # # Scrape the professor's ratings
    # overall_rating = driver.find_element(By.CLASS_NAME, "RatingValue__Numerator-qw8sqy-2 liyUjw").text

    # print(f"Professor: {professor_name}")
    # print(f"Overall Rating: {overall_rating}")

    # print(f"nice")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()