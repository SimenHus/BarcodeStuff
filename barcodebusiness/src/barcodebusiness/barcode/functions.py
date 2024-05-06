import httpx

async def fetch_barcode_info(API_key: str, barcode: str) -> dict:
    headers = {'Authorization': f'Bearer {API_key}'}
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://kassal.app/api/v1/products/ean/{barcode}', headers=headers)

    return response.json()

