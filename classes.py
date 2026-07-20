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
class PanelConfig():
    """ Configuration for application panels and borders """
    banner_height: float # Top panel height
    border_width: float  # Right edge width
    panel_width: float   # Left navigation panel width


@dataclass
class ViewportConfig():
    padding: float
    n_btns_per_row: float
    btn_separation: tuple # (horizontal, vertical) space between button edges in pixels
