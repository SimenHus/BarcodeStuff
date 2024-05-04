from scraping.common import ScraperBase, Product

from selenium.webdriver.common.by import By

class MenyScraper(ScraperBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def scrape(self, rootPage):
        print('Getting root...')
        self.driver.get(rootPage)
        self.wait(By.CLASS_NAME, 'ws-product-vertical__link')
        print('Root loaded')

        subPages = self.driver.find_elements(
            By.CSS_SELECTOR, 'a.ws-product-vertical__link')
        page = subPages[0].get_attribute('href')

        productJSON = self.scrapeProduct(page)

    def scrapeProduct(self, productPage):
        product = Product(website=productPage)

        print('Loading subpage...')
        self.driver.get(productPage)
        self.wait(By.CLASS_NAME, 'ngr-accordion-item__header--inline')
        print('Subpage loaded')

        dropDownMenus = self.driver.find_elements(By.CSS_SELECTOR,
            'button.ngr-accordion-item__header--inline')
        for menu in dropDownMenus: menu.click()


        productInfo = self.driver.find_elements(
            By.CSS_SELECTOR, 'td.ws-manufacturer-info__item-label')
        productInfoValue = self.driver.find_elements(
            By.CSS_SELECTOR, 'td.ws-manufacturer-info__item-value')
        for label, value in zip(productInfo, productInfoValue):
            if label.text[:-1] == 'Merke': product.brand = value.text
            if label.text[:-1] == 'GTIN': product.barcode = value.text

        nutritionInfo = self.driver.find_elements(
            By.CSS_SELECTOR, 'li.ws-nutritional-content__list-view-item')
        for i, label in enumerate(nutritionInfo):

            info = label.text.split(':\n')
            text, value = info[0], float(info[1].split()[0])
            category = None
            if text == "Energi": category = 'energy'
            if text == "Kalorier": category = 'calories'
            if text == "Fett": category = 'fat'
            if text == "Mettet fett": category = "saturated-fat"
            if text == "Karbohydrater": category = "carbs"
            if text == "Sukkerarter": category = "sugar"
            if text == "Sukkeralkoholer": category = "sugar-alcohols"
            if text == "Stivelse": category = "starch"
            if text == "Kostfiber": category = "dietary-fiber"
            if text == "Protein": category = "protein"
            if text == "Salt": category = "salt"
            if category is None: continue
            product.nutrition[category] = value

        print(product)