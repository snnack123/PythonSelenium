from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt

class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element

    def pull_data(self):
        try:
            collection = []

            for box in self.boxes_section_element:
                hotel_name = box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML')
                hotel_score = box.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"] > div').get_attribute('innerHTML')
                hotel_price = box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').replace('&nbsp;', ' ')
                hotel_address = box.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').get_attribute('innerHTML')
                hotel_location = box.find_element(By.CSS_SELECTOR, 'span[data-testid="distance"]').get_attribute('innerHTML')
                collection.append([ hotel_name, hotel_score, hotel_price, hotel_address, hotel_location ])
            return collection
        except Exception as e:
            print("There is a problem pulling data from the results: " + str(e))

    def print_cluster(self, x, y):
        plt.scatter(x, y)
        plt.show()
