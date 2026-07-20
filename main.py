import os
import pygame as pg
from Artist import Artist
from Button import Button
from classes import ArrowKeyState, ViewportConfig, PanelConfig

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
pg.init()


class MediaViewer():
    def __init__(self):
        self.artist = Artist()
        self.clock = pg.time.Clock()

        # Layout constants
        self.view_cfg = ViewportConfig(
            padding=50,
            n_btns_per_row=5,
            n_cols=3,
            btn_separation=(150, 300)
        )
        self.panel_cfg = PanelConfig(
            banner_height=int(self.artist.SCREEN_Y * 0.08),
            border_width=int(self.artist.SCREEN_Y * 0.02),
            panel_width=int(self.artist.SCREEN_Y * 0.08)
        )
        self.btn_height = 200


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
                l_color="#001D4A",
                r_color="#001D4A",
                t_color="#003687",
                b_color="#001D4A",
                order=("left", "right", "top", "bottom")
            )
            if frame_count == 0:
                self.draw_buttons(buttons, available_rect)

            frame_count += 1
            pg.display.update()

    
    def draw_buttons(self, buttons: list[Button], available_rect: pg.Rect):
        """ Draw all buttons in the matrix on the available viewport area """
        pad = self.view_cfg.padding
        n_per_row = self.view_cfg.n_btns_per_row
        n_cols = self.view_cfg.n_cols
        n_total = n_per_row * n_cols
        btn_sep = self.view_cfg.btn_separation
        available_rect.top += pad
        available_rect.left += pad
        available_rect.width -= pad * 2
        available_rect.height -= pad * 2

        avail_btn_width = available_rect.width - btn_sep[0] * (n_per_row - 1)
        btn_width = round(avail_btn_width / n_per_row)
        for i in range(n_total):
            x = available_rect.left + (i % n_per_row) * (btn_width + btn_sep[0])
            y = available_rect.top + (i // n_per_row) * btn_sep[1]
            buttons.append(
                Button(
                    self.artist, f"{i}",
                    x, y, btn_width, self.btn_height,
                    border_radius=26
                )
            )
        
        return buttons
    

    def set_focus_idx(self, arrow_state: ArrowKeyState, focus_idx: list[int]):
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


if __name__ == "__main__":
    viewer = MediaViewer()
    viewer.start_viewer()
