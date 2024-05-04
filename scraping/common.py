from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dataclasses import dataclass, field

class ScraperBase:


    def __init__(self, driver):
        self.driver = driver


    def wait(self, method, value):
        elem = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (method, value)
            )
        )

        return elem

@dataclass
class Product:
    barcode: str = '0000000000000'
    brand: str = 'N/A'
    price: float = 0.0
    weight: float = 0.0
    nutrition: dict = field(default_factory=lambda: {
        "energy": -1.0,
        "calories": -1.0,
        "fat": -1.0,
        "saturated-fat": -1.0,
        "carbs": -1.0,
        "sugar": -1.0,
        "sugar-alcohols": -1.0,
        "starch": -1.0,
        "dietary-fiber": -1.0,
        "protein": -1.0,
        "salt": -1.0
    })
    allergies: dict = field(default_factory=lambda: {
        "contains": [],
        "traces": []
    })
    website: str = 'N/A'
