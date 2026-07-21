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
