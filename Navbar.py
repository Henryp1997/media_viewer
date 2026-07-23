"""
Navbar.py

Defines a Navbar class to hold Buttons and allow the user
to navigate between types of media and to settings

    - Author: HP (2026)
"""
from Artist import Artist
from classes import NavbarConfig, BorderConfig
from Button import Button


class Navbar():
    def __init__(
        self,
        artist: Artist,
        navbar_config: NavbarConfig,
        border_config: BorderConfig
    ) -> None:
        self.artist = artist
        self.cfg = navbar_config
        self.border_cfg = border_config
        self.create_buttons()


    def draw(self, focus_idx: list[int]):
        """ Draw the Navbar and its buttons """
        self.artist.draw_rect(
            color=self.cfg.bg_color, x=0, y=0,
            w=self.cfg.navbar_width, h=self.artist.display.SCREEN_Y
        )
        for i, btn in enumerate(self.buttons):
            btn.in_focus = False
            if focus_idx[1] == -1:
                btn.in_focus = focus_idx[0] == i
            btn.draw()

    
    def create_buttons(self):
        """ Create all Navbar buttons """
        pad = self.cfg.padding
        width = self.cfg.navbar_width - 2 * pad
        height = width
        self.buttons = [
            Button(
                self.artist, text="x",
                x=pad,
                y=self.border_cfg.banner_height + pad,
                w=width, h=height,
                border_radius=8, bg_colour="#00FF00"
            )
        ]
