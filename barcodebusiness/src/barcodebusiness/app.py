"""
Barcode reading and stuff
"""

import PIL.Image
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import PIL
import numpy as np

from barcodebusiness.barcode import *

class BarcodeBusiness(toga.App):
    def startup(self):
        # Main layout widgets
        main_box = toga.OptionContainer() # Main box to contain all sub boxes
        input_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        products_box = toga.Box(style=Pack(direction=ROW, flex=1))

        # Widgets for input_box
        barcode_label = toga.Label(
            'Barcode to check: ',
            style=Pack(padding=(0, 5))
        )
        self.barcode_input = toga.TextInput(style=Pack(flex=1))

        barcode_box = toga.Box(style=Pack(direction=ROW, padding=5))
        barcode_box.add(barcode_label)
        barcode_box.add(self.barcode_input)

        button = toga.Button(
            'Fetch',
            on_press=self.check_barcode,
            style=Pack(padding=5)
        )

        input_box.add(barcode_box)
        input_box.add(button)

        # Widgets for products_box
        self.scanned_products_table = toga.Table(
            headings=['Product name', 'Quantity']
        )

        headings = ['Nutrition category', 'Amount', 'Unit']
        accessors = {headings[0]: 'category', headings[1]: 'amount', headings[2]: 'unit'}
        products_nutrient_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.products_nutrient_base = toga.Table(
            headings=headings,
            accessors=accessors
        )
        self.products_nutrient_total = toga.Table(
            headings=headings,
            accessors=accessors
        )
        products_nutrient_box.add(self.products_nutrient_base)
        products_nutrient_box.add(self.products_nutrient_total)

        products_box.add(self.scanned_products_table)
        products_box.add(products_nutrient_box)

        main_box.content.append('Input', input_box)
        main_box.content.append('Product', products_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def capture_video(self) -> None:
        """Function to capture video and scan for barcodes"""
        
        image = None
        try:
            image = await self.camera.take_photo() # Returns None if canceled photo
        except PermissionError as error: # Raises PermissionError if camera permission has not been granted
            self.main_window.info_dialog( # Notify the user in regards to camera permission
                'Permission denied',
                'The app needs permission to use the camera'
            )
        
        if image is None: return # If image is not none we successfully captured an image

        image = np.array(image.as_format(PIL.Image.Image)) # Convert image to format readable by cv2
        barcodes = await detect_barcode(image) # Detect barcodes in image

    async def check_barcode(self, widget) -> None:
        barcode = self.barcode_input.value
        is_sane, comment = await sanity_check(barcode)
        if not is_sane:
            self.main_window.info_dialog(
                'Barcode error',
                comment
            )
            return
        
        barcode_data = await fetch_barcode_data(barcode)
        product = await parse_barcode_data(barcode_data)

        data_base, data_total = product.nutrition_data()

        self.products_nutrient_base.data = data_base
        self.products_nutrient_total.data = data_total



def main():
    return BarcodeBusiness()
