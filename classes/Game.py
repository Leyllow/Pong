from tkinter import *
from time import *
import random


class Game():
    window = Tk()
    window_width = 800
    window_height = 600

    main_canvas = object

    ball = object
    ball_dimensions = 20
    ball_initial_coords = {}
    ball_x_direction = random.choice([-10, 10])
    ball_y_direction = 0
    ball_speed = 0
    ball_initial_speed = 75
    bounces = 0

    p1_bar = object
    p1_bar_initial_coords = {}
    p2_bar = object
    p2_bar_initial_coords = {}
    bars_len = 100

    p1_score = 0
    p2_score = 0
    p1_score_label = object
    p2_score_label = object

    def __init__(self):
        self.window.geometry("%sx%s+300+125" % (self.window_width, self.window_height))

        self.main_canvas = Canvas(
            self.window, bg='black', width=self.window_width, height=self.window_height)
        self.main_canvas.pack(fill='both')

        self.window.update_idletasks()

        self.draw_middle_line()

        scores_font = ('times', 50, 'bold')
        self.p1_score_label = self.display_score(scores_font, 'p1')
        self.p1_score_label.place(relx=.25, rely=.1)
        self.p2_score_label = self.display_score(scores_font, 'p2')
        self.p2_score_label.place(relx=.75, rely=.1)

        self.ball_initial_coords = {'x1': int(self.window_width) / 2 - self.ball_dimensions / 2,
                                    'y1': int(self.window_height) / 2 - self.ball_dimensions / 2,
                                    'x2': int(self.window_width) / 2 + self.ball_dimensions / 2,
                                    'y2': int(self.window_height) / 2 + self.ball_dimensions / 2}
        self.ball = self.draw_ball()

        self.ball_speed = self.ball_initial_speed

        self.p1_bar = self.draw_bars('p1')
        self.p2_bar = self.draw_bars('p2')

    def draw_ball(self):
        return self.main_canvas.create_rectangle(
            self.ball_initial_coords['x1'], self.ball_initial_coords['y1'],
            self.ball_initial_coords['x2'], self.ball_initial_coords['y2'], fill="white")

    def draw_bars(self, player):
        bar_coords = {}

        if player == 'p1':
            bar_coords = {'x1': 10, 'y1': int(self.window_height) / 2 - self.bars_len / 2, 
                'x2': 20, 'y2': int(self.window_height) / 2 + self.bars_len / 2}
            self.p1_bar_initial_coords = bar_coords
        else:
            bar_coords = {'x1': int(self.window_width) - 10, 'y1': int(self.window_height) / 2 - 50,
                           'x2': int(self.window_width) - 20, 'y2': int(self.window_height) / 2 + 50}
            self.p2_bar_initial_coords = bar_coords
        
        return self.main_canvas.create_rectangle(bar_coords['x1'], bar_coords['y1'],
                                                 bar_coords['x2'], bar_coords['y2'], fill="white")

    def draw_middle_line(self):
        line_w, line_h = 4 / 2, 550 / 2
        self.main_canvas.create_rectangle(int(self.window_width) / 2 - line_w, int(self.window_height) / 2 - line_h,
                                          int(self.window_width) / 2 + line_w, int(self.window_height) / 2 + line_h, fill="white")

    def display_score(self, font, player):
        return Label(self.window, text=self.p1_score if player == 'p1' else self.p2_score,
                     font=font, bg='black', fg='white')

    def change_score(self, player):
        if player == "p1":
            self.p1_score += 1
            self.p1_score_label.config(text=self.p1_score)
        elif player == "p2":
            self.p2_score += 1
            self.p2_score_label.config(text=self.p2_score)

    def move_bars(self, event):
        key = event.keysym
        up = -20
        down = 20

        if key == "q":
            if self.get_bar_coords('p1')['y1'] > 0:
                self.main_canvas.move(self.p1_bar, 0, up)
        elif key == "w":
            if self.get_bar_coords('p1')['y2'] < self.window_height:
                self.main_canvas.move(self.p1_bar, 0, down)

        if key == "Up":
            if self.get_bar_coords('p2')['y1'] > 0:
                self.main_canvas.move(self.p2_bar, 0, up)
        elif key == "Down":
            if self.get_bar_coords('p2')['y2'] < self.window_height:
                self.main_canvas.move(self.p2_bar, 0, down)

    def get_ball_coords(self):
        ball_coords = self.main_canvas.coords(self.ball)
        return {'x1': ball_coords[0], 'y1': ball_coords[1], 'x2': ball_coords[2], 'y2': ball_coords[3]}

    def get_bar_coords(self, player):
        bar_coords = self.main_canvas.coords(
            self.p1_bar if player == 'p1' else self.p2_bar)
        return {'x1': bar_coords[0], 'y1': bar_coords[1], 'x2': bar_coords[2], 'y2': bar_coords[3]}

    def increase_ball_speed(self):
        if self.bounces > 0 and self.bounces % 2 == 0:
            self.ball_speed = self.ball_speed - 5 if self.ball_speed > 25 else 25

    def ball_bounced(self, bar):
        self.bounces += 1
        self.increase_ball_speed()
        self.change_ball_direction(10 if bar == 'bar1' else -10)

    def change_ball_angle(self, y):
        self.ball_y_direction = y

    def change_ball_direction(self, x):
        self.ball_x_direction = x
    
    def check_zone_bounce(self, bar, bar_coords, ball_coords):
        if bar == 'bar1':
            if ball_coords['y2'] == bar_coords['y1'] + self.bars_len / 2 - self.ball_dimensions / 2: 
                self.change_ball_angle(self.ball_y_direction - 10)
            if ball_coords['y1'] == bar_coords['y1'] + self.bars_len / 2 + self.ball_dimensions / 2:
                self.change_ball_angle(self.ball_y_direction + 10)
        else:
            if ball_coords['y1'] == bar_coords['y1'] + self.bars_len / 2 + self.ball_dimensions / 2: 
                self.change_ball_angle(self.ball_y_direction + 10)
            if ball_coords['y2'] == bar_coords['y1'] + self.bars_len / 2 - self.ball_dimensions / 2: 
                self.change_ball_angle(self.ball_y_direction - 10)
            
    def check_window_limit(self, ball_coords):
        if ball_coords['y1'] <= 0:
            self.change_ball_angle(self.ball_y_direction + abs(self.ball_y_direction) * 2)
        elif ball_coords['y2'] >= self.window_height:
            self.change_ball_angle(self.ball_y_direction - self.ball_y_direction * 2)

    def check_p1_bar_bounce(self, ball_coords, bar_coords):
        return (ball_coords['x1'] == bar_coords['x2']
            and ball_coords['y1'] < bar_coords['y2']
            and ball_coords['y2'] > bar_coords['y1'])

    def check_p2_bar_bounce(self, ball_coords, bar_coords):
        return (ball_coords['x2'] == bar_coords['x1']
            and ball_coords['y1'] < bar_coords['y2']
            and ball_coords['y2'] > bar_coords['y1'])

    def ball_movement(self):
        ball_coords = self.get_ball_coords()
        p1_bar_coords = self.get_bar_coords('p1')
        p2_bar_coords = self.get_bar_coords('p2')

        self.check_window_limit(ball_coords)

        if self.check_p1_bar_bounce(ball_coords, p1_bar_coords):
            self.ball_bounced('bar1')
            self.check_zone_bounce('bar1', p1_bar_coords, ball_coords)
        if self.check_p2_bar_bounce(ball_coords, p2_bar_coords):
            self.ball_bounced('bar2')
            self.check_zone_bounce('bar2', p2_bar_coords, ball_coords)
        if ball_coords['x1'] < p1_bar_coords['x2']:
            self.end_run('p2')
        if ball_coords['x2'] > p2_bar_coords['x1']:
            self.end_run('p1')

    def reset_bars(self):
        self.main_canvas.delete(self.p1_bar)
        self.p1_bar = self.draw_bars('p1')
        self.main_canvas.delete(self.p2_bar)
        self.p2_bar = self.draw_bars('p2')

    def end_run(self, winner):
        sleep(1)
        self.change_score(winner)
        self.change_ball_direction(0)
        self.change_ball_angle(0)
        self.bounces = 0
        self.ball_speed = self.ball_initial_speed
        self.main_canvas.delete(self.ball)
        self.ball = self.draw_ball()
        self.reset_bars()
        self.ball_x_direction = random.choice([-10, 10])

    def move_ball(self):
        self.ball_movement()
        self.main_canvas.move(self.ball, self.ball_x_direction, self.ball_y_direction)
        self.window.after(self.ball_speed, self.move_ball)

    def key_binding(self):
        self.window.bind("<Key>", self.move_bars)

    def start_game(self):
        self.key_binding()
        self.move_ball()
        self.window.mainloop()
