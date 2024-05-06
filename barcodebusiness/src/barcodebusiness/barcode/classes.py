
from dataclasses import dataclass
import cv2

@dataclass
class BarcodeItem:
    code: str

    def __post_init__(self):
        if type(self.code) == int: self.code = str(self.code)

    def __repr__(self):
        return f'Barcode id: {self.code}'


class BarcodeDetector(cv2.barcode.BarcodeDetector):
    API_key = 'rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl'

    async def detect(self, img) -> 'list[BarcodeItem]':
        retval, codes, straight_code, points = await super().detectAndDecodeWithType(img)
        
        if not retval: return []

        detections = []
        for code in codes: detections.append(BarcodeItem(code))

        return detections
