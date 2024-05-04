
from cv2 import barcode
from barcodes.barcode import Barcode
import numpy as np

class BarcodeDetector(barcode.BarcodeDetector):
    pass

    def detect(self, img):
        retval, codes, straight_code, points = super().detectAndDecodeWithType(img)
        
        if not retval: return []

        detections = []
        for i, code in enumerate(codes): detections.append(Barcode(code, np.array([points[i]])))

        return detections
    