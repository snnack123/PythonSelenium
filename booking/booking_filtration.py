from selenium.webdriver.common.by import By
import time

class BookingFiltration:
    def __init__(self, driver):
        self.driver = driver

    def apply_star_rating(self, stars=2):
        star_rating_element = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-item="class:class=' + str(stars) + '"] > label > span:nth-of-type(2)')
        star_rating_element.click()
        time.sleep(1)

    def sort_price_lowest_first(self):
        sort_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        sort_element.click()

        lowest_price_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        lowest_price_element.click()