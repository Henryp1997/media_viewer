"""
AdapatablePixel.py

Defines a single AdaptablePixelSize class to scale fixed pixel
sizes based on the current display scaling factor

To use:
    First initialise:
        APS(None, display)
    Scale any fixed size:
        scaled_size = APS(fixed_size)

E.g., if display.scaling == 1.25, APS(100) = 100 / 1.25 = 80

Once a value is converted using APS, any later calculations
with that value will also be in scaled units
E.g.,
    width = APS(100)
    height = width * 4/3 <-- height will also be in appropriately scaled units
"""

from Display import Display


class AdaptablePixelSize():
    display: Display | None = None

    def __new__(cls, pixel_size: int, display: Display | None = None):
        if cls.display is None:
            if display is None:
                raise ValueError("AdaptablePixelSize expected 'Display' object in args got None")
            cls.display = display
        
        if pixel_size is not None:
            adjusted = pixel_size / cls.display.scaling
            return round(adjusted)
