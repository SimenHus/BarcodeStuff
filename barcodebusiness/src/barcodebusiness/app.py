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
        main_box = toga.Box(style=Pack(direction=COLUMN))

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

        self.table_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        main_box.add(barcode_box)
        main_box.add(button)
        main_box.add(self.table_box)

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

        table = await self.generate_nutrition_table(product)

        self.table_box.add(table)




    
    async def generate_nutrition_table(self, product: Product) -> toga.Table:

        headings = ['Nutrition', 'Value', 'Unit']
        accessors = {
            'Nutrition': 'category',
            'Value': 'amount',
            'Unit': 'unit'
        }
        data = product.nutrition_table()

        table = toga.Table(
            headings=headings,
            accessors=accessors,
            data=data
        )

        return table




def main():
    return BarcodeBusiness()
