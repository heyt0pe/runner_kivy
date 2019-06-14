from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
import random

Window.size = 900, 350
plyr = ''

class Start(Button):
    pass

class Player(Widget):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        global plyr
        plyr = self

shouldMove = False

class Obstacle(Widget):
    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.move()
        global plyr

    def move(self, *args):
        global speed
        Clock.schedule_interval(self.movement, 1/60)

    def movement(self, *args):
        global shouldMove
        if shouldMove:
            self.pos[0] -= 8
            if self.collide_widget(plyr):
                shouldMove = False
        else:
            Clock.unschedule(self.movement)

obs = []

class Frame(Widget):
    canJump = True
    timer = 0
    score = 0

    def __init__(self, **kwargs):
        super(Frame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def start(self, *args):
        try:
            b = self.ids['start']
            self.remove_widget(b)
        except:
            pass
        finally:
            global obs
            for i in obs:
                self.remove_widget(i)
            obs = []
            global shouldMove
            shouldMove = True
            self.canJump = True
            self.timer = 0
            self.score = 0
            p = self.ids['player']
            p.pos = 200, 5
            Clock.schedule_interval(self.obstacleCreation, 1/10)

    def obstacleCreation(self, *args):
        global shouldMove, obs
        for _ in obs:
            if _.pos[0] < -2:
                self.remove_widget(_)
                obs.remove(_)
        if shouldMove:
            self.score += 1
            player = self.ids['player']
            s = self.ids['score']
            s.text = '00{}'.format(str(self.score))
            if self.score >= 30:
                if self.score % 15 == 0:
                    first = random.randrange(901, 950)
                    second = first + 24
                    third = second + 24
                    no = random.randrange(1, 4)
                    for i in range(no):
                        if i == 0:
                            h = random.randrange(70, 101)
                            x = Obstacle(size_hint = (None, None), size = (22, h))
                            x.pos = (first, 0)
                        elif i == 1:
                            h = random.randrange(70, 101)
                            x = Obstacle(size_hint = (None, None), size = (22, h))
                            x.pos = (second, 0)
                        elif i == 2:
                            h = random.randrange(70, 101)
                            x = Obstacle(size_hint = (None, None), size = (22, h))
                            x.pos = (third, 0)
                        obs.append(x)
                        self.add_widget(x)
        else:
            Clock.unschedule(self.obstacleCreation)

    def _keyboard_closed(self, *args):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers, *args):
        global shouldMove
        if shouldMove:
            if keycode[1] == 'spacebar' or keycode[1] == 'w' or keycode[1] == 'up':
                if self.canJump:
                    self.canJump = False
                    player = self.ids['player']
                    player.pos[1] += 10
                    Clock.schedule_interval(self.up, 1/40)
        else:
            self.start()

    def up(self, *args):
        self.timer += 0.025
        player = self.ids['player']
        global shouldMove
        if shouldMove:
            if self.timer > 0 and self.timer < 0.5:
                player.pos[1] += 10
            elif self.timer >= 0.5 and self.timer < 1:
                player.pos[1] -= 10
            else:
                self.timer = 0
                Clock.unschedule(self.up)
                self.canJump = True
        else:
            Clock.unschedule(self.up)


Builder.load_file('runner.kv')

class Runners(App):
    def build(self):
        return Frame()

Runners().run()
