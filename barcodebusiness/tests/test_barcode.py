from barcodebusiness.barcode.functions import fetch_barcode_info
import asyncio

def test_fetch():
    """If a barcode number is provided, check that it is fetched from the database"""
    result = asyncio.run(fetch_barcode_info('rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl', '7035620021985'))
    assert result['data']['ean'] == '7035620021985'