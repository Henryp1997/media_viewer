import pygame as pg


class Artist():
    def __init__(
        self,
        SCREEN_X: int | None = None,
        SCREEN_Y: int | None = None
    ) -> None:
        self.SCREEN_X = SCREEN_X
        self.SCREEN_Y = SCREEN_Y
        if None in (SCREEN_X, SCREEN_Y):
            info = pg.display.Info()
            self.screen = pg.display.set_mode(
                (
                    info.current_w,
                    info.current_h
                ), pg.NOFRAME
            )
            self.SCREEN_X = info.current_w
            self.SCREEN_Y = info.current_h
             

    def fill_screen(self, color) -> None:
        self.screen.fill(color)


    def draw_rect(self, color, x, y, w, h, linewidth=0, border_radius=0):
        """
        Draw a rectangle. Default is to fill with the specified
        color (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.rect(
            self.screen,
            color,
            pg.Rect((x, y, w, h)),
            border_radius=border_radius,
            width=linewidth
        )


    def draw_border(self, color, linewidth=1, border_radius=0, offset=0) -> None:
        w, h = self.screen.get_size()
        self.draw_rect(
            color, x=offset, y=offset, w=w-2*offset, h=h-2*offset,
            linewidth=linewidth, border_radius=border_radius
        )


    def draw_circle(self, color, cx, cy, radius, linewidth=0):
        """
        Draw a circle. Default is to fill with the specified
        color (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.circle(self.screen, color, (cx, cy), radius, width=linewidth)


    def draw_filled_borders(
        self,
        l_width: int,
        r_width: int,
        t_height: int,
        b_height: int,
        padding: tuple | list,
        l_color: str,
        r_color: str,
        t_color: str,
        b_color: str,
        order: tuple = ("left", "right", "top", "bottom")
    ):
        """ Draw four borders in the available window space """
        def draw_left():
            self.draw_rect(
                color=l_color, x=0, y=0,
                w=l_width, h=self.SCREEN_Y
            )
        def draw_right():
            self.draw_rect(
                color=r_color,
                x=self.SCREEN_X - r_width, y=0,
                w=r_width, h=self.SCREEN_Y
            )
        def draw_top():
            self.draw_rect(
                color=t_color, x=0, y=0,
                w=self.SCREEN_X, h=t_height
            )
        def draw_bottom():
            self.draw_rect(
                color=b_color,
                x=0, y=self.SCREEN_Y - b_height,
                w=self.SCREEN_X, h=b_height
            )
        draw_methods = {
            "left": draw_left, "right": draw_right,
            "top": draw_top, "bottom": draw_bottom
        }
        for side in order:
            draw_methods[side]()

        # Compute available rect for GUI elements
        available_rect = pg.Rect(
            l_width,  # x
            t_height, # y
            self.SCREEN_X - r_width - l_width,  # Width
            self.SCREEN_Y - b_height - t_height # Height
        )

        # Adjust rect for padding
        available_rect.left += padding[0]
        available_rect.top += padding[1]
        available_rect.width -= padding[0] * 2
        available_rect.height -= padding[1] * 2

        return available_rect


    def blit(self, *args, **kwargs):
        self.screen.blit(*args, **kwargs)
