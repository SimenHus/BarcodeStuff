"""
Barcode reading and stuff
"""

import PIL.Image
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import PIL
import numpy as np

from barcodebusiness.barcode import detect_barcode

class BarcodeBusiness(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)


        button = toga.Button(
            'Say hello!',
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

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


def main():
    return BarcodeBusiness()
