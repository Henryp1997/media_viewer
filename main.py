import os
import pygame as pg
from Artist import Artist
from Button import Button
from classes import ArrowKeyState, ViewportConfig, PanelConfig, ButtonSizeConfig

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
pg.init()


class MediaViewer():
    def __init__(self):
        self.artist = Artist()
        self.clock = pg.time.Clock()

        # Layout constants
        self.panel_cfg = PanelConfig(
            banner_height=int(self.artist.SCREEN_Y * 0.08),
            border_width=int(self.artist.SCREEN_Y * 0.02),
            panel_width=int(self.artist.SCREEN_Y * 0.08)
        )
        self.view_cfg = ViewportConfig(
            padding=[130, 80],
            n_btns_per_row=4,
            n_cols=3,
        )

        # Button sizing configuratino
        width = 280
        height = int(0.75 * width)
        self.btn_cfg = ButtonSizeConfig(
            width=width, height=height,
            separation=None # Calculated later
        )
        


    def start_viewer(self):
        frame_count = 0
        persist_btn_dark = {}
        buttons = []
        focus_idx = [0, 0]    # Which button in the matrix is currently in focus
        btn_persist_click = 3 # Number of frames for button to appear pressed
        arrow_state = ArrowKeyState()
        while True:
            self.clock.tick(60)
            self.artist.fill_screen(color="#1F1F1F")
            self.artist.draw_border("#FF0000", offset=6)

            mouse_click_pos = None
            arrow_state.clear() # Crucial for debounce
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_click_pos = event.pos
                elif event.type == pg.KEYDOWN:
                    for key, name in zip(
                        (pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN),
                        ("right", "left", "up", "down")
                    ):
                        arrow_state.__dict__[name] = (event.key == key)
                elif event.type == pg.QUIT:
                    pg.quit()
                    return
            
            # Check pressed keys. Only register key press if key not pressed on previous frame
            focus_idx = self.set_focus_idx(arrow_state, focus_idx)
            
            if buttons:
                # Draw buttons and change color if clicked
                for i, btn in enumerate(buttons):
                    clicked = False
                    if mouse_click_pos:
                        clicked = btn.check_clicked(mouse_click_pos)
                    
                    if clicked:
                        # Button was clicked with mouse cursor, shift focus
                        focus_idx = [
                            i // self.view_cfg.n_btns_per_row,
                            i % self.view_cfg.n_btns_per_row
                        ]
                        persist_btn_dark[btn] = frame_count
                    
                    btn.in_focus = (i == focus_idx[0] * self.view_cfg.n_btns_per_row + focus_idx[1])

                    draw_method = "draw_clicked"
                    if frame_count - persist_btn_dark.get(btn, 0) > btn_persist_click:
                        # Frame count check to draw 'clicked' version of button longer than just one frame
                        persist_btn_dark[btn] = 0
                        draw_method = "draw"

                    getattr(btn, draw_method)()
            
            available_rect = self.artist.draw_filled_borders(
                l_width=self.panel_cfg.panel_width,
                r_width=self.panel_cfg.border_width,
                t_height=self.panel_cfg.banner_height,
                b_height=self.panel_cfg.border_width,
                padding=self.view_cfg.padding,
                l_color="#001D4A",
                r_color="#001D4A",
                t_color="#003687",
                b_color="#001D4A",
                order=("left", "right", "top", "bottom")
            )
            if frame_count == 0:
                self.calc_btn_separation(available_rect)
                self.draw_buttons(buttons, available_rect)

            frame_count += 1
            pg.display.update()

    
    def draw_buttons(self, buttons: list[Button], available_rect: pg.Rect):
        """ Draw all buttons in the matrix on the available viewport area """
        n_per_row = self.view_cfg.n_btns_per_row
        n_cols = self.view_cfg.n_cols
        n_total = n_per_row * n_cols
        btn_sep = self.btn_cfg.separation
        btn_width = self.btn_cfg.width

        for i in range(n_total):
            x = available_rect.left + (i % n_per_row) * (btn_width + btn_sep[0])
            y = available_rect.top + (i // n_per_row) * btn_sep[1]
            buttons.append(
                Button(
                    self.artist, f"{i}",
                    x, y, btn_width, self.btn_cfg.height,
                    border_radius=26
                )
            )
        
        return buttons
    

    def set_focus_idx(self, arrow_state: ArrowKeyState, focus_idx: list[int]):
        """ 
        Set the value of the focus_idx list which points to the
        matrix location of the button most recently given focus
        """
        for name, axis, value in zip(
            ("right", "left", "up", "down"),
            (1, 1, 0, 0),
            (1, -1, -1, 1)
        ):
            if arrow_state.__dict__[name]:
                focus_idx[axis] += value
        
        focus_idx[0] = max(0, focus_idx[0])
        focus_idx[1] = min(max(0, focus_idx[1]), self.view_cfg.n_btns_per_row - 1)
        return focus_idx


    def calc_btn_separation(self, available_rect: pg.Rect) -> tuple[int]:
        """
        Calculate the required horizontal and vertical separation
        between buttons given the padding and button width/height
        """
        n_per_row = self.view_cfg.n_btns_per_row
        max_allowed_btn_width = int(available_rect.width / n_per_row)
        if self.btn_cfg.width > max_allowed_btn_width:
            # If the user has configured a width that is too wide, the
            # separation must be zero and the width must be capped
            self.btn_cfg.separation = (0, 400)
            self.btn_cfg.width = max_allowed_btn_width
            return

        width = self.btn_cfg.width
        horiz_sep = int(
            (available_rect.width - (n_per_row * width)) / (n_per_row - 1)
        )
        self.btn_cfg.separation = (horiz_sep, 400)


if __name__ == "__main__":
    viewer = MediaViewer()
    viewer.start_viewer()
