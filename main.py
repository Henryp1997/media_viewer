import os
import time
import pygame as pg
from Artist import Artist
from Button import Button

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
pg.init()


class MediaViewer():
    def __init__(self):
        self.artist = Artist()
        self.clock = pg.time.Clock()


    def start_viewer(self):
        frame_count = 0
        persist_btn_dark = {}
        buttons = []
        for i in range(1):
            buttons.append(
                Button(self.artist, "hello", 100, 100 + i * 150, 200, 100, border_radius=26)
            )
        
        banner_height = int(self.artist.SCREEN_Y * 0.08)
        border_width = int(self.artist.SCREEN_Y * 0.02)
        panel_width = int(self.artist.SCREEN_Y * 0.08)

        btn_persist_click = 3   # Number of frames for button to appear pressed
        obj_move_scroll_px = 5 # Number of pixels to move an object when scrolling the mouse wheel
        while True:
            self.clock.tick(60)
            self.artist.fill_screen(color="#1F1F1F")
            self.artist.draw_border("#FF0000", offset=6)

            mouse_click_pos = None
            scroll_direction = None
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_click_pos = event.pos
                elif event.type == pg.QUIT:
                    pg.quit()
                    return
            
            # Check pressed keys
            pressed = pg.key.get_pressed()
            if pressed[pg.K_DOWN]:
                scroll_direction = 1
            if pressed[pg.K_UP]:
                scroll_direction = -1
            if pressed[pg.K_DOWN] and pressed[pg.K_UP]:
                scroll_direction = None
            
            # Move items down if scrolling
            if scroll_direction is not None:
                buttons[0].y += scroll_direction * obj_move_scroll_px
                screen_rect = self.artist.screen.get_rect()
                ymin, ymax = screen_rect.y, screen_rect.height
                if buttons[0].y < ymin:
                    buttons[0].y = ymin
                elif buttons[0].y + buttons[0].h > ymax:
                    buttons[0].y = ymax - buttons[0].h
            
            # Draw buttons and change color if clicked
            for btn in buttons:
                clicked = False
                if mouse_click_pos:
                    clicked = btn.check_clicked(mouse_click_pos)
                
                if clicked:
                    persist_btn_dark[btn] = frame_count

                draw_method = "draw_clicked"
                if frame_count - persist_btn_dark.get(btn, 0) > btn_persist_click:
                    persist_btn_dark[btn] = 0
                    draw_method = "draw"

                getattr(btn, draw_method)()
            
            available_rect = self.artist.draw_filled_borders(
                l_width=panel_width,
                r_width=border_width,
                t_height=banner_height,
                b_height=border_width,
                l_color="#001D4A",
                r_color="#001D4A",
                t_color="#003687",
                b_color="#001D4A",
                order=("left", "right", "top", "bottom")
            )
            if frame_count == 0:
                print(available_rect)

            frame_count += 1
            pg.display.update()

if __name__ == "__main__":
    viewer = MediaViewer()
    viewer.start_viewer()
