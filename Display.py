import ctypes
import pygame as pg

class Display():
    def __init__(
        self,
        SCREEN_X: int | None = None,
        SCREEN_Y: int | None = None
    ):
        self.SCREEN_X = SCREEN_X
        self.SCREEN_Y = SCREEN_Y
        if None in (SCREEN_X, SCREEN_Y):
            self.info = pg.display.Info()
            self.screen = pg.display.set_mode(
                (
                    self.info.current_w,
                    self.info.current_h
                ), pg.NOFRAME
            )
            self.SCREEN_X = self.info.current_w
            self.SCREEN_Y = self.info.current_h

        self.scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
