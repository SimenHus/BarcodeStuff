import httpx
import json

def fetch_barcode_info(barcode: str) -> dict:
    """Function to fetch info from a supplied barcode"""
    
    API_key = 'rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl'

    headers = {'Authorization': f'Bearer {API_key}'}
    with httpx.Client() as client:
        response = client.get(f'https://kassal.app/api/v1/products/ean/{barcode}', headers=headers)

    return response.json()



res = fetch_barcode_info('7038010000065')
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)