import httpx
from cv2.barcode import BarcodeDetector
import numpy as np

async def fetch_barcode_info(barcode: str) -> dict:
    """Function to fetch info from a supplied barcode"""
    
    API_key = 'rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl'

    headers = {'Authorization': f'Bearer {API_key}'}
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://kassal.app/api/v1/products/ean/{barcode}', headers=headers)

    return response.json()


async def detect_barcode(img: np.ndarray) -> 'list[str]':
    """Function to detect barcode in a supplied image"""
    retval, codes, straight_code, points = await BarcodeDetector().detectAndDecodeWithType(img)
    
    if not retval: return []

    detections = []
    for code in codes: detections.append(code)

    return detections