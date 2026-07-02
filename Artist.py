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
             

    def fill_screen(self, colour) -> None:
        self.screen.fill(colour)


    def draw_rect(self, colour, x, y, w, h, linewidth=0, border_radius=0):
        """
        Draw a rectangle. Default is to fill with the specified
        colour (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.rect(
            self.screen,
            colour,
            pg.Rect((x, y, w, h)),
            border_radius=border_radius,
            width=linewidth
        )


    def draw_border(self, colour, linewidth=1, border_radius=0, offset=0) -> None:
        w, h = self.screen.get_size()
        self.draw_rect(
            colour, x=offset, y=offset, w=w-2*offset, h=h-2*offset,
            linewidth=linewidth, border_radius=border_radius
        )


    def draw_circle(self, colour, cx, cy, radius, linewidth=0):
        """
        Draw a circle. Default is to fill with the specified
        colour (linewidth=0). Set linewidth > 0 to draw just the outline
        """
        pg.draw.circle(self.screen, colour, (cx, cy), radius, width=linewidth)


    def blit(self, *args, **kwargs):
        self.screen.blit(*args, **kwargs)
