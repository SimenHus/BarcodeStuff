from dataclasses import dataclass
from toga.sources import ListSource
from copy import copy

@dataclass
class Product:
    ean: str
    name: str
    unit: str
    quantity: float
    allergens: tuple
    nutrition: ListSource
    _image_source: str = None
    accessors = ['category', 'amount', 'unit'] # Class variable

    def __post_init__(self) -> None:
        if type(self.ean) == int: self.ean = str(self.ean)

        factor = self.quantity / 100
        self.nutrition_total = copy(self.nutrition)
        for nutrition in self.nutrition_total:
            self.nutrition_total.find() = factor*nutrition.amount


    def __repr__(self) -> str:
        return f'Barcode id: {self.ean}'