import logging
import os
import random
import time
import sys

from screen import Screen
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
from config.configHemiPVT import CONF

#########################################################################

# Initialize screen, logger and inputs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["task"]["name"]), CONF=CONF)  # This is for saving data
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()  # starts clock for timestamping events
Alarm = sound.Sound('600', secs=0.01, sampleRate=44100,
                    stereo=True)  # TODO: make it alarm-like

# Experiment conditions
showLeft = random.choice([True, False])

logging.info('Initialization completed')

#########################################################################

##############
# Introduction
##############

# # Display overview of session
# screen.show_overview()
# core.wait(CONF["timing"]["overview"])

# # Optionally, display instructions
# if CONF["showInstructions"]:
#     screen.show_instructions()
#     key = event.waitKeys()
#     if key[0] == 'q':
#         logging.warning('Force quit after instructions')
#         sys.exit(1)

# # Blank screen for initial rest
# screen.show_blank()
# logging.info('Starting blank period')

# # TODO: send start trigger
# core.wait(CONF["timing"]["rest"])
# # TODO: send end wait trigger

# # Cue start of the experiment
# screen.show_cue("START")
# core.wait(CONF["timing"]["cue"])

##########################################################################

#################
# Main experiment
#################

sequence_number = 0

for x in range(1, CONF["task"]["blocks"]):

    showLeft = not showLeft  # switches to the opposite side after each block
    blockTimer = core.CountdownTimer(CONF["task"]["duration"])

    while blockTimer.getTime() > 0:

        sequence_number += 1
        logging.info('Starting iteration #%s with leftOn=#%s',
                     sequence_number, showLeft)

        ###############################
        # Wait a random period of time

        delay = random.uniform(
            CONF["fixation"]["minDelay"], CONF["fixation"]["maxDelay"])

        # log
        datalog["block"] = x
        datalog["sequence_number"] = sequence_number
        datalog["delay"] = delay
        logging.info('Starting delay of %s seconds', delay)

        # show correctly illuminated screen
        if showLeft:
            datalog["hemifield"] = "left"
            screen.show_left()
            x = random.uniform(-2, 0) - CONF["task"]["maxRadius"]
        else:
            datalog["hemifield"] = "right"
            screen.show_right()
        y = random.choice([-1, 1])*(random.uniform(0, 2) -
                                    CONF["task"]["maxRadius"])

        # start
        delayTimer = core.CountdownTimer(delay)

        extraKeys = []
        while delayTimer.getTime() > 0:

            # Record any extra key presses during wait
            extraKey = kb.getKeys()
            if extraKey:
                if extraKey[0].name == 'q':
                    logging.warning('Forced quit during wait')
                    sys.exit(2)

                extraKeys.append(mainClock.getTime())

                # Flash the fixation box to indicate unexpected key press
                screen.flash_fixation_box(CONF["task"]["earlyColor"])
                core.wait(CONF["fixation"]["errorFlash"])
                screen.flash_fixation_box(CONF["fixation"]["fillColor"])

            core.wait(0.0005)

        #######################
        # Stimulus presentation

        # initialize stopwatch
        Missed = False

        def onFlip():  # TODO: does this go somewhere else?
            kb.clock.reset()
            datalog["startTime"] = mainClock.getTime()
            # TODO: send trigger

        # run stopwatch
        Timer = core.CountdownTimer(CONF["task"]["maxTime"])
        screen.window.callOnFlip(onFlip)
        print(x, y)
        screen.start_spot(x, y)
        keys = []
        while not keys:
            keys = kb.getKeys(waitRelease=False)
            if Timer.getTime() <= 0:
                Missed = True
                break

            radiusPercent = Timer.getTime()/CONF["task"]["maxTime"]
            screen.shrink_spot(radiusPercent)

        #########
        # Outcome

        if Missed:  # TODO: make alarm if no keypress for mroe than 5 seconds
            logging.info("missed")
            datalog["skipped"] = True

        else:
            # show result
            reactionTime = keys[0].rt
            screen.show_result(reactionTime)
            core.wait(CONF["fixation"]["scoreTime"])

            if keys[0].name == 'q':
                logging.warning('Forced quit during task')
                sys.exit(3)

            # save to memory
            datalog["rt"] = reactionTime
            datalog["response_key"] = keys[0].name

        # save data to file
        datalog["extrakeypresses"] = extraKeys
        datalog.flush()

###########
# Concluion

# End main experiment
screen.show_cue("DONE!")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')
# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

logging.info('Finished')
