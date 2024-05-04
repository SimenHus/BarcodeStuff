import cv2

from common import *
from barcodes import BarcodeDetector



detector = BarcodeDetector()
img = cv2.imread(IMGS[2])


detections = detector.detect(img)

if len(detections) == 0:
    print('No barcodes detected')
    exit()

print('Barcode detected')


for barcode in detections:
    img = cv2.polylines(img, barcode.pts.astype(int), True, (0, 255, 0), 3)

img = cv2.resize(img, (600, 600))
cv2.imshow('image', img)
cv2.waitKey(0)