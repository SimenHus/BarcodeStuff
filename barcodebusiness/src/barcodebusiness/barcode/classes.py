
from dataclasses import dataclass

@dataclass
class BarcodeItem:
    code: str

    def __post_init__(self):
        if type(self.code) == int: self.code = str(self.code)

    def __repr__(self):
        return f'Barcode id: {self.code}'
