from barcodebusiness.barcode.functions import fetch_barcode_data, sanity_check
import asyncio

def test_fetch():
    """If a barcode number is provided, check that it is fetched from the database"""
    result = asyncio.run(fetch_barcode_data('7035620021985'))
    assert result['data']['ean'] == '7035620021985'


def test_sanity_proper():
    """If a barcode number is provided, check that it is compliant with EAN-13"""
    result = asyncio.run(sanity_check('7035620021985'))
    assert result[0] == True

def test_sanity_wrong():
    """If a barcode number is provided, check that it is compliant with EAN-13"""
    result = asyncio.run(sanity_check('7035620021986'))
    assert result[0] == False

