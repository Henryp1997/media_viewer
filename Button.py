from pathlib import Path
import pygame as pg
import numpy as np
from Artist import Artist
from AdaptablePixel import AdaptablePixelSize as APS

HERE = Path(__file__).parent

class Button():
    def __init__(
        self,
        artist: Artist,
        text: str,
        x: int,
        y: int,
        w: int,
        h: int,
        border_radius: int = 12,
        bg_colour: str = "#0080FF",
        fg_colour: str = "#FFFFFF",
        focus_border_color: str = "#FFFFFF",
        in_focus: bool = False, # Draw an outline if True
        is_navbar_btn: bool = False
    ):
        self.artist = artist
        self.text = text
        self.x, self.y, self.w, self.h = x, y, w, h
        self.r = self.x + self.w
        self.b = self.y + self.h
        self.border_radius = border_radius
        self.focus_border_color = focus_border_color
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.font = pg.font.Font(HERE / "Consolas-Regular.ttf", 16)
        self.in_focus = in_focus
        self.is_navbar_btn = is_navbar_btn


    def move(self, axis: int, delta: int):
        """
        Move this Button horizontally (axis = 0) or vertically (axis = 1)
        `delta` can be positive or negative but care needs to be taken with
        the y-axis as PyGame defines (0, 0) as the top left corner of the
        window, therefore positive `delta` for the y-axis means 'move downwards'
        """
        if axis == 0:
            self.x += delta
            self.r += delta
        elif axis == 1:
            self.y += delta
            self.b += delta
        else:
            raise ValueError(f"Invalid axis value. Got {axis!r}, expected 0 or 1.")


    def draw(self, bg_colour: str | None = None):
        """ Draw the button """
        if bg_colour is None:
            bg_colour = self.bg_colour

        self.artist.draw_rect(
            bg_colour, self.x, self.y, self.w, self.h,
            border_radius=self.border_radius
        )

        if self.in_focus:
            self.draw_focus_border()

        cx = self.x + 0.5 * self.w
        cy = self.y + 0.5 * self.h
        text_obj = self.font.render(self.text, True, self.fg_colour, None)
        text_rect = text_obj.get_rect()
        text_rect.center = (cx, cy)
        self.artist.blit(text_obj, text_rect)


    def draw_clicked(self):
        """ Draw the button in a darker shade to simulate depression of the button """
        bg = self.bg_colour
        rgb = np.array([float(int(bg[i] + bg[i+1], 16)) for i in range(1, len(bg), 2)])
        rgb *= 0.7
        
        new_bg = "#"
        for c in rgb:
            c_str = hex(int(c))[2:]
            if len(c_str) == 1:
                c_str = f"0{c_str}"
            new_bg += c_str

        self.draw(bg_colour=new_bg)


    def draw_focus_border(self):
        """ Draw a border around the button when in focus. Uses configurable self.focus_border_color """
        self.artist.draw_rect(
            self.focus_border_color, self.x, self.y, self.w, self.h,
            linewidth=APS(3),
            border_radius=self.border_radius
        )


    def check_clicked(self, pos: tuple):
        """ Check if the user clicked within the bounds of this Button """
        x, y = pos
        if not self.x <= x <= self.r:
            return False
        if not self.y <= y <= self.b:
            return False
        return True
