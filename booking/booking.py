import os
from selenium import webdriver
import booking.constants as const
from selenium.webdriver.common.by import By
import time
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    # constructor of the class
    def __init__(self, driver_path = r"C:\SeleniumDrivers", teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        selected_currency_element = self.find_element(By.XPATH, "//div[text()='" + currency + "']")
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        self.accept_cookies()
        search_field = self.find_element(By.CSS_SELECTOR, 'input[name="ss"]')
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(1)

        option = self.find_element(By.CSS_SELECTOR, 'ul[data-testid="autocomplete-results"] > li')
        option.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, 'span[data-date="' + check_in_date + '"]')
        check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, 'span[data-date="' + check_out_date + '"]')
        check_out_element.click()

    def select_adults(self, adults=1):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        container = self.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"]')
        adults_decrease_button = container.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"] > div > div:nth-of-type(1) > div:nth-of-type(2) > button:nth-of-type(1)')
        adults_increase_button = container.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"] > div > div:nth-of-type(1) > div:nth-of-type(2) > button:nth-of-type(2)')

        adults = int(adults)

        if adults > 2:
            for _ in range(adults - 2):
                adults_increase_button.click()
        elif adults < 2:
            for _ in range(2 - adults):
                adults_decrease_button.click()

    def select_rooms(self, rooms=1):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        container = self.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"]')
        # rooms_decrease_button = container.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"] > div > div:nth-of-type(3) > div:nth-of-type(2) > button:nth-of-type(1)')
        rooms_increase_button = container.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"] > div > div:nth-of-type(3) > div:nth-of-type(2) > button:nth-of-type(2)')

        rooms = int(rooms)

        if rooms > 1:
            for _ in range(rooms - 1):
                rooms_increase_button.click()

        search_button = self.find_element(By.CSS_SELECTOR, 'div[data-testid="occupancy-popup"] > button')
        search_button.click()

    def click_search_button(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtrations(self, stars=2):
        stars = int(stars)
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(stars=stars)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

        report = BookingReport(hotel_boxes)
        collections = report.pull_data()
        table = PrettyTable(field_names=["Hotel Name", "Score", "Price", "Address", "Distance"])
        table.add_rows(collections)
        print(table)
        x = [float(sublist[1]) for sublist in collections]
        y = [float(sublist[2].rstrip(' lei').replace(",", ".")) for sublist in collections]
        report.print_cluster(x, y)
        while(True): 
            pass

    def accept_cookies(self):
        cookies_button = self.find_element(By.CSS_SELECTOR, 'button[id="onetrust-accept-btn-handler"]')
        if cookies_button:
            cookies_button.click()