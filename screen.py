from psychopy import visual, core, event
from psychopy.hardware import keyboard
from psychopy.visual import textbox


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            color=CONF["fixation"]["colorOff"],
            # display_resolution=CONF["screen"]["resolution"],
            # monitor=CONF["screen"]["monitor"],
            fullscr=CONF["screen"]["full"], units="norm",
            allowGUI=True
        )

        # set up instructions and overview
        self.task = visual.TextStim(self.window,
                                    # pos=[0, 0],
                                    text=CONF["task"]["name"],
                                    alignHoriz='center',
                                    alignVert='center',
                                    height=.3,
                                    pos=(0, 0),  # TEMP
                                    units="norm"
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " + CONF["session"],
                                       pos=[.75, -.3],  # TEMP
                                       height=.1,
                                       alignHoriz='center',
                                       alignVert='center',
                                       units="norm"
                                       )

        self.instructions = visual.TextStim(
            self.window, text=CONF["instructions"]["text"], height=.05)

        self.startPrompt = visual.TextStim(
            self.window, text=CONF["instructions"]["startPrompt"], height=0.05, pos=[0, -.3])

        self.cue = visual.TextStim(self.window)

        # Setup background
        self.fixation_box = visual.Rect(
            self.window, height=CONF["fixation"]["height"],
            width=CONF["fixation"]["width"],
            fillColor=CONF["fixation"]["boxColor"],
            lineColor=CONF["fixation"]["boxColor"],
            units=CONF["screen"]["units"])

        self.left_on = visual.Rect(
            self.window, height=2,
            width=1,
            pos=(-.5, 0),
            fillColor=CONF["fixation"]["colorOn"],
            lineColor=CONF["fixation"]["colorOn"],
            units="norm")

        self.right_on = visual.Rect(
            self.window, height=2,
            width=1,
            pos=(.5, 0),
            fillColor=CONF["fixation"]["colorOn"],
            lineColor=CONF["fixation"]["colorOn"],
            units="norm")

        # setup stopwatch
        self.spot = visual.Circle(
            self.window,
            edges=100,
            units="cm"
        )

    def show_overview(self):
        self.task.draw()
        self.session.draw()
        self.window.flip()

    def show_instructions(self):
        self.instructions.draw()
        self.startPrompt.draw()
        self.window.flip()

    def show_blank(self):
        self.window.flip()

    def show_cue(self, word):
        self.cue.setText(word)
        self.cue.draw()
        self.window.flip()

    def show_left(self):
        self.backgroundLeft = True
        self._draw_background()
        self.window.flip()

    def show_right(self):
        self.backgroundLeft = False
        self._draw_background()
        self.window.flip()

    def flash_fixation_box(self):
        self._flip_fixation_color(self.CONF["task"]["earlyColor"])
        core.wait(self.CONF["fixation"]["errorFlash"])
        self._flip_fixation_color(self.CONF["fixation"]["boxColor"])

    def start_spot(self, x, y):
        self.spot.pos = [x, y]
        self.spot.radius = self.CONF["task"]["maxRadius"]
        self._set_spot_color(self.CONF["task"]["color"])
        self._draw_background()
        self.spot.draw()
        self.window.flip()

    def shrink_spot(self, size, colored=False):
        self.spot.radius = self.CONF["task"]["maxRadius"]*size

        self._draw_background()
        self.spot.draw()
        self.window.flip()

    def _set_spot_color(self, color):
        self.spot.fillColor = color
        self.spot.lineColor = color

    def _flip_fixation_color(self, color):
        self.fixation_box.fillColor = color
        self.fixation_box.lineColor = color
        self._draw_background()
        self.fixation_box.draw()
        self.window.flip()

    def _draw_background(self):
        if self.backgroundLeft:
            self.left_on.draw()
        else:
            self.right_on.draw()

        self.fixation_box.draw()

    def show_result(self, time):
        # gives different color stimulus depending on result
        radiusPercent = (self.CONF["task"]["maxTime"] -
                         time) / self.CONF["task"]["maxTime"]
        if time < self.CONF["task"]["minTime"]:
            self.flash_fixation_box()
            return
        elif time < self.CONF["task"]["maxTime"]:
            self._set_spot_color(self.CONF["task"]["victoryColor"])
        else:
            return

        self.shrink_spot(radiusPercent)
