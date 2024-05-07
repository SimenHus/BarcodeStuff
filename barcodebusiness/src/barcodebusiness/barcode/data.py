
from dataclasses import dataclass

@dataclass
class Product:
    ean: str
    name: str
    quantity: float = 0.0
    unit: str = 'g'
    image_source: str = None
    allergens: tuple = ()
    nutrition: tuple = ()

    def __post_init__(self) -> None:
        if type(self.ean) == int: self.ean = str(self.ean)

    def __repr__(self) -> str:
        return f'Barcode id: {self.ean}'
    
    def nutrition_table(self) -> list:
        table = []
        for nutrition in self.nutrition:
            table.append({
                'category': nutrition['display_name'],
                'amount': nutrition['amount'],
                'unit': nutrition['unit']
            })
        return table