

from dataclasses import dataclass
import numpy as np

@dataclass
class Barcode:
    code: str
    pts: np.ndarray
    

    def __post_init__(self):
        if type(self.code) == int: self.code = str(self.code)

    def __repr__(self):
        return f'Barcode id: {self.code}'
