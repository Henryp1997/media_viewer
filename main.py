import os
import pygame as pg
from Display import Display
from Artist import Artist
from Navbar import Navbar
from Button import Button
from AdaptablePixel import AdaptablePixelSize as APS
from classes import ArrowKeyState, ViewportConfig, BorderConfig, NavbarConfig, ButtonSizeConfig
from consts import ASPECT_RATIOS, DEFAULT_WIDTHS

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
pg.init()


class MediaViewer():
    def __init__(self):
        self.display = Display()
        APS(None, display=self.display) # Initialise AdaptablePixelSize engine
        self.artist = Artist(self.display)
        self.clock = pg.time.Clock()
        self.available_rect = None

        # Layout configuration
        self.border_cfg = BorderConfig(
            banner_height=int(self.display.SCREEN_Y * 0.08),
            border_width=int(self.display.SCREEN_Y * 0.02),
            navbar_width=int(self.display.SCREEN_Y * 0.08),
            top_color="#003687",
            bottom_color="#001D4A",
            right_color="#001D4A"
        )
        self.view_cfg = ViewportConfig(
            padding=[APS(130), APS(50)],
            n_btns_per_row=4,
            n_rows=3,
        )
        self.navbar_cfg = NavbarConfig(
            navbar_width=self.border_cfg.navbar_width,
            padding=APS(10),
            bg_color="#001D4A"
        )

        self.navbar = Navbar(self.artist, self.navbar_cfg, self.border_cfg)

        # Button sizing configuration. Use standard 3:4 movie box art aspect ratio
        self.media_type = "movie"
        width = APS(DEFAULT_WIDTHS[self.media_type])
        height = ASPECT_RATIOS[self.media_type] * width
        self.btn_cfg = ButtonSizeConfig(
            width=width, height=height,
            separation=None # Calculated later
        )

        # Initialise variables
        self.frame_count = 0
        self.btn_persist_click = 3 # Number of frames for button to appear pressed
        self.arrow_state = ArrowKeyState()


    def start_viewer(self):
        """ Start the application and run the game loop """
        buttons = []
        persist_btn_dark = {} # Record of the frame number in which a button was pressed
        focus_idx = [0, 0]    # Which button in the matrix is currently in focus
        while True:
            self.clock.tick(60)
            self.artist.fill_screen(color="#1F1F1F")

            # Update elements
            events = pg.event.get()
            mouse_click_pos = self.update_arrow_state(events)
            self.set_focus_idx(self.arrow_state, focus_idx)
            if buttons:
                focus_idx = self.update_buttons(
                    buttons, mouse_click_pos, persist_btn_dark, focus_idx
                )
            
            # Draw elements
            self.draw_buttons(buttons, persist_btn_dark)
            self.available_rect = self.draw_borders()
            if self.frame_count == 0:
                self.calc_btn_separation()
                self.init_draw_buttons(buttons)
            self.navbar.draw(focus_idx=focus_idx)

            self.check_quit(events)
            self.frame_count += 1
            pg.display.update()

    
    def update_arrow_state(self, events):
        """ Update the state of directional arrow inputs """
        mouse_click_pos = None
        self.arrow_state.clear() # Crucial for debounce
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_click_pos = event.pos
            elif event.type == pg.KEYDOWN:
                for key, name in zip(
                    (pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN),
                    ("right", "left", "up", "down")
                ):
                    self.arrow_state.__dict__[name] = (event.key == key)
        return mouse_click_pos


    def update_buttons(
        self,
        buttons: list[Button],
        mouse_click_pos: tuple[int],
        persist_btn_dark: dict,
        focus_idx: list[int]
    ) -> list[int]:
        """ Update the state of all clickable media Buttons """
        scroll_direction = None
        for i, btn in enumerate(buttons + self.navbar.buttons):
            if mouse_click_pos and btn.check_clicked(mouse_click_pos):
                # Button was clicked with mouse cursor, shift focus by changing focus_idx
                if btn.is_navbar_btn:
                    focus_idx[0] = i - len(buttons)
                    focus_idx[1] = -1
                else:
                    focus_idx = [
                        i // self.view_cfg.n_btns_per_row,
                        i % self.view_cfg.n_btns_per_row
                    ]
                
                persist_btn_dark[btn] = self.frame_count
            
            focused_idx = focus_idx[0] * self.view_cfg.n_btns_per_row + focus_idx[1]
            btn.in_focus = i == focused_idx and focus_idx[1] != -1
            if btn.in_focus and btn.b > self.available_rect.bottom:
                # Button is partially obscured by the bottom border. Initiate a row scroll upwards
                scroll_direction = -1
            elif btn.in_focus and btn.y < self.available_rect.top:
                # Button is partially obscured by the top banner. Initiate a row scroll downwards
                scroll_direction = 1

        if scroll_direction is not None:
            self.scroll_buttons(buttons, scroll_direction)
        
        return focus_idx


    def scroll_buttons(self, buttons: list[Button], scroll_direction: int):
        """
        User has highlighted a button which is above or below the rows
        of fully visible buttons. This method will scroll all buttons by
        one row grid separation to bring the highlighted button into view
        """
        for btn in buttons:
            y_sep = scroll_direction * self.btn_cfg.separation[1] / 1.5
            btn.move(axis=1, delta=y_sep)


    def draw_buttons(self, buttons: list[Button], persist_btn_dark: dict) -> None:
        """ Draw all buttons after updating their state """
        for btn in buttons:
            draw_method = "draw_clicked"
            if self.frame_count - persist_btn_dark.get(btn, 0) > self.btn_persist_click:
                # Frame count check to draw 'clicked' version of button longer than just one frame
                persist_btn_dark[btn] = 0
                draw_method = "draw"
            getattr(btn, draw_method)()


    def init_draw_buttons(self, buttons: list[Button]):
        """ Draw all buttons in the matrix on the available viewport area """
        n_per_row = self.view_cfg.n_btns_per_row
        n_rows = self.view_cfg.n_rows
        n_total = n_per_row * n_rows
        btn_sep = self.btn_cfg.separation
        btn_width = self.btn_cfg.width

        for i in range(n_total):
            x = self.available_rect.left + (i % n_per_row) * (btn_width + btn_sep[0])
            y = self.available_rect.top + (i // n_per_row) * btn_sep[1]
            buttons.append(
                Button(
                    self.artist, f"{i}",
                    x, y, btn_width, self.btn_cfg.height,
                    border_radius=26
                )
            )
            

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
        
        focus_idx[1] = max(-1, focus_idx[1])
        focus_idx[0] = min(max(0, focus_idx[0]), self.view_cfg.n_rows - 1)


    def draw_borders(self) -> pg.Rect:
        """ Draw application borders and calculate the available area for GUI elements """
        available_rect = self.artist.draw_filled_borders(
            l_width=self.border_cfg.navbar_width,
            r_width=self.border_cfg.border_width,
            t_height=self.border_cfg.banner_height,
            b_height=self.border_cfg.border_width,
            padding=self.view_cfg.padding,
            r_color=self.border_cfg.right_color,
            t_color=self.border_cfg.top_color,
            b_color=self.border_cfg.bottom_color,
            order=("right", "top", "bottom")
        )
        return available_rect


    def calc_btn_separation(self) -> tuple[int]:
        """
        Calculate the required horizontal and vertical separation
        between buttons given the padding and button width/height
        """
        n_per_row = self.view_cfg.n_btns_per_row
        max_allowed_btn_width = int(self.available_rect.width / n_per_row)
        if self.btn_cfg.width > max_allowed_btn_width:
            # If the user has configured a width that is too wide, the
            # separation must be zero and the width must be capped
            self.btn_cfg.separation = (0, APS(400))
            self.btn_cfg.width = max_allowed_btn_width
            return

        width = self.btn_cfg.width
        horiz_sep = int(
            (self.available_rect.width - (n_per_row * width)) / (n_per_row - 1)
        )
        self.btn_cfg.separation = (horiz_sep, APS(400))


    def check_quit(self, events):
        """ Check for the quit event """
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                return


if __name__ == "__main__":
    viewer = MediaViewer()
    viewer.start_viewer()
