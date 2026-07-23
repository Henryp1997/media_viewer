import pygame as pg
from Display import Display

class Artist():
    def __init__(self, display: Display) -> None:
        self.display = display
             

    def fill_screen(self, color) -> None:
        self.display.screen.fill(color)


    def draw_rect(self, color, x, y, w, h, linewidth=0, border_radius=0):
        """
        Draw a rectangle. Default is to fill with the specified
        color (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.rect(
            self.display.screen,
            color,
            pg.Rect((x, y, w, h)),
            border_radius=border_radius,
            width=linewidth
        )


    def draw_border(self, color, linewidth=1, border_radius=0, offset=0) -> None:
        w, h = self.display.screen.get_size()
        self.draw_rect(
            color, x=offset, y=offset, w=w-2*offset, h=h-2*offset,
            linewidth=linewidth, border_radius=border_radius
        )


    def draw_circle(self, color, cx, cy, radius, linewidth=0):
        """
        Draw a circle. Default is to fill with the specified
        color (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.circle(self.display.screen, color, (cx, cy), radius, width=linewidth)


    def draw_filled_borders(
        self,
        l_width: int,
        r_width: int,
        t_height: int,
        b_height: int,
        padding: tuple | list,
        r_color: str,
        t_color: str,
        b_color: str,
        order: tuple = ("right", "top", "bottom")
    ):
        """
        Draw three borders in the available window space. Do not
        draw the left border as that is handled by Navbar.draw()
        """
        def draw_right():
            self.draw_rect(
                color=r_color,
                x=self.display.SCREEN_X - r_width, y=0,
                w=r_width, h=self.display.SCREEN_Y
            )
        def draw_top():
            self.draw_rect(
                color=t_color, x=0, y=0,
                w=self.display.SCREEN_X, h=t_height
            )
        def draw_bottom():
            self.draw_rect(
                color=b_color,
                x=0, y=self.display.SCREEN_Y - b_height,
                w=self.display.SCREEN_X, h=b_height
            )
        draw_methods = {
            "right": draw_right,
            "top": draw_top, "bottom": draw_bottom
        }
        for side in order:
            draw_methods[side]()

        # Compute available rect for GUI elements
        available_rect = pg.Rect(
            l_width,  # x
            t_height, # y
            self.display.SCREEN_X - r_width - l_width,  # Width
            self.display.SCREEN_Y - b_height - t_height # Height
        )
        self.draw_rect(
            "#888888",
            l_width,  # x
            t_height, # y
            self.display.SCREEN_X - r_width - l_width,  # Width
            self.display.SCREEN_Y - b_height - t_height, # Height
            linewidth=2
        )

        # Adjust rect for padding
        available_rect.left += padding[0]
        available_rect.top += padding[1]
        available_rect.width -= padding[0] * 2

        # No padding for bottom since the app contents will be painted there if there are enough items 
        available_rect.height -= padding[1]

        return available_rect


    def blit(self, *args, **kwargs):
        self.display.screen.blit(*args, **kwargs)
