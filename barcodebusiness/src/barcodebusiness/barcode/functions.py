import httpx
from cv2.barcode import BarcodeDetector
from barcodebusiness.barcode.data import Product
import numpy as np
from toga.sources import ListSource

async def fetch_barcode_data(barcode: str) -> dict:
    """Function to fetch info from a supplied barcode"""
    
    API_key = 'rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl'

    headers = {'Authorization': f'Bearer {API_key}'}
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://kassal.app/api/v1/products/ean/{barcode}', headers=headers)

    return response.json()


async def detect_barcode(img: np.ndarray) -> list[str]:
    """Function to detect barcode in a supplied image"""
    retval, codes, straight_code, points = await BarcodeDetector().detectAndDecodeWithType(img)
    
    if not retval: return []

    detections = []
    for code in codes: detections.append(code)

    return detections


async def parse_barcode_data(data: str) -> Product:
    """Function to parse barcode data and store in format suitable for display table"""
    data = data['data'] # Shorten dict calls
    ean = data['ean'] # Get ean number

    allergens = [] # Allergens contained
    for allergen in data['allergens']: # Loop through allergens to see if any are present
        if allergen['contains'].upper() == "YES": allergens.append(allergen)
    
    name = data['products'][0]['name']
    image_source = data['products'][0]['image']
    for product in data['products']: # Check if any stores have listed quantity of product
        if product['weight'] is None: continue # No quantity found
        unit = product['weight_unit']
        quantity = product['weight']
        if unit.lower() == 'l' or 'kg': # Convert from L/kg to mL/g
            unit = unit[1:]
            quantity *= 1000
        image_source = product['image']
        name = product['name']

    nutrition_data = []
    for nutrition in data['nutrition']:
        nutrition_data.append({
            'category': nutrition['display_name'],
            'amount': float(nutrition['amount']),
            'unit': nutrition['unit']
        })

    nutrition = ListSource(
        accessors=Product.accessors,
        data=nutrition_data
    )


    product_data = Product(
        ean=ean,
        name=name,
        quantity=quantity,
        unit=unit,
        allergens=allergens,
        nutrition=nutrition,
        _image_source=image_source
    )

    return product_data


async def sanity_check(barcode: str) -> 'list[bool, str["comment"]]':
    """Check if the supplied barcode is correctly formatted"""
    if type(barcode) == int: barcode = str(barcode)
    if len(barcode) < 13: return False, 'Barcode is too short'
    if len(barcode) > 13: return False, 'Barcode is too long'
    try: int(barcode)
    except ValueError: return False, 'Barcode is not a number'

    weights = [1, 3]
    sum = 0
    for i, digit in enumerate(barcode[:-1]): # Sum barcode digits according to EAN-13
        sum += int(digit)*weights[i%len(weights)]
    if (sum + int(barcode[-1]))%10 != 0: return False, 'Barcode sum is not correct according to EAN-13'
    return True, 'Barcode is compliant with EAN-13'
