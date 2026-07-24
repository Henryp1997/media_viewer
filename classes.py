from dataclasses import dataclass, fields

@dataclass
class ArrowKeyState():
    """ Class for holding arrow key pressed state """
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False

    def clear(self):
        for field in fields(self):
            setattr(self, field.name, False)


@dataclass
class BorderConfig():
    """ Configuration for application panels and borders """
    banner_height: float # Top panel height
    border_width: float  # Right edge width
    navbar_width: float  # Left navigation bar width
    right_color: str
    top_color: str
    bottom_color: str


@dataclass
class NavbarConfig():
    """ Configuration for the navigation bar """
    navbar_width: float # Left navigation bar width
    padding: float      # Padding between buttons and edge of navbar
    bg_color: str


@dataclass
class ViewportConfig():
    """ Configuration for the available viewing area """
    padding: tuple | list # Padding on the [left/right, top/bottom] of the available viewport
    n_btns_per_row: float # Number of buttons per row
    n_rows: float         # Number of rows of buttons


@dataclass
class ButtonSizeConfig():
    """ Configuration for the size of and separation between buttons """
    width: float
    height: float
    separation: tuple # (Horizontal, vertical) space between button edges
