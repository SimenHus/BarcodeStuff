from cv2.barcode import BarcodeDetector
import cv2

detector = BarcodeDetector()
img = cv2.imread('assets\\test_image_multiple_01.png')

detections = BarcodeDetector.detect(img)


for barcode in detections:
    img = cv2.polylines(img, barcode.pts.astype(int), True, (0, 255, 0), 3)

img = cv2.resize(img, (600, 600))
cv2.imshow('image', img)
cv2.waitKey(0)