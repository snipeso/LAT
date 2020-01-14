import logging
import os
import random
import time
import sys

from screen import Screen
from scorer import Scorer
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
from config.configHemiPVT import CONF

#########################################################################

# Initialize screen, logger and inputs
logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["task"]["name"]), CONF=CONF)  # This is for saving data
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()  # starts clock for timestamping events
Alarm = sound.Sound(os.path.join('sounds', CONF["tones"]["alarm"]),
                    stereo=True)  # TODO: make it alarm-like
# TODO: make it alarm-like
scorer = Scorer()

# Experiment conditions
showLeft = random.choice([True, False])


logging.info('Initialization completed')

#########################################################################


def quitExperimentIf(toQuit):
    "Quit experiment if condition is met"

    if toQuit:

        scorer.getScore()  # TODO: see if this is ok to do
        logging.info('quit experiment')
        sys.exit(2)  # TODO: make version where quit is sys 1 vs sys 2

##############
# Introduction
##############


# Display overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# Optionally, display instructions
if CONF["showInstructions"]:
    screen.show_instructions()
    key = event.waitKeys()
    quitExperimentIf(key[0] == 'q')

# Blank screen for initial rest
screen.show_blank()
logging.info('Starting blank period')

# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

# Cue start of the experiment
screen.show_cue("START")
core.wait(CONF["timing"]["cue"])

##########################################################################

#################
# Main experiment
#################


sequence_number = 0
totBlocks = CONF["task"]["blocks"]
for block in range(totBlocks):
    block += 1
    logging.info(f"{block} / {totBlocks}")
    showLeft = not showLeft  # switches to the opposite side after each block
    totMissed = 0
    blockTimer = core.CountdownTimer(CONF["task"]["duration"])

    while blockTimer.getTime() > 0:

        sequence_number += 1
        logging.info('Starting iteration #%s with leftOn=#%s',
                     sequence_number, showLeft)

        ###############################
        # Wait a random period of time

        # create delay for wait
        delay = random.uniform(
            CONF["fixation"]["minDelay"],
            CONF["fixation"]["maxDelay"]) - CONF["task"]["extraTime"]  # the extra time delay happens after stimulus presentation

        # show correctly illuminated screen
        rightBorder = CONF["screen"]["size"][0] / 2
        topBorder = CONF["screen"]["size"][1] / 2

        if showLeft:
            datalog["hemifield"] = "left"
            screen.show_left()
            x = random.uniform(-rightBorder + CONF["task"]["maxRadius"],
                               0 - CONF["task"]["maxRadius"])
        else:
            datalog["hemifield"] = "right"
            screen.show_right()
            x = random.uniform(
                0 + CONF["task"]["maxRadius"], rightBorder - CONF["task"]["maxRadius"])

        y = random.uniform(-topBorder + CONF["task"]["maxRadius"],
                           topBorder - CONF["task"]["maxRadius"])

        # log
        datalog["block"] = block
        datalog["sequence_number"] = sequence_number
        datalog["delay"] = delay
        datalog["position"] = [x, y]
        logging.info(
            'Starting delay of %s seconds in position x=%s, y=%s', delay, x, y)

        # start
        delayTimer = core.CountdownTimer(delay)

        extraKeys = []
        tones = []
        while delayTimer.getTime() > 0:

            # play randomly tones in the mean time
            toneDelay = random.uniform(
                CONF["tones"]["minTime"], CONF["tones"]["maxTime"])
            toneTimer = core.CountdownTimer(toneDelay)

            while delayTimer.getTime() > 0 and toneTimer.getTime() > 0:
                # Record any extra key presses during wait
                extraKey = kb.getKeys()
                if extraKey:
                    quitExperimentIf(extraKey[0].name == 'q')

                    extraKeys.append(mainClock.getTime())

                    # Flash the fixation box to indicate unexpected key press
                    screen.flash_fixation_box()

            # TODO: play tone & send trigger
            tones.append(mainClock.getTime())
            logging.info("tone at %s", mainClock.getTime())

        # log data
        datalog["tones"] = tones
        datalog["extrakeypresses"] = extraKeys
        scorer.scores["extraKeys"] += len(extraKeys)

        #######################
        # Stimulus presentation

        # initialize stopwatch
        Missed = False
        Late = False

        def onFlip():  # TODO: does this go somewhere else?
            kb.clock.reset()  # this starts the keyboard clock as soon as stimulus appears
            datalog["startTime"] = mainClock.getTime()
            # TODO: send start trigger

        # run stopwatch
        logging.info("waiting for shrinking to start")
        Timer = core.CountdownTimer(CONF["task"]["maxTime"])
        screen.window.callOnFlip(onFlip)

        screen.start_spot(x, y)
        keys = []

        while not keys:
            keys = kb.getKeys(waitRelease=False)
            T = Timer.getTime()

            if T <= -CONF["task"]["extraTime"]:  # stop waiting for keys
                Missed = True
                break
            elif T <= 0:  # keep waiting for keys, but don't show stimulus
                Late = True
                radiusPercent = 0
            else:  # shrink stimulus
                radiusPercent = T/CONF["task"]["maxTime"]

            screen.shrink_spot(radiusPercent)
        # TODO: response trigger

        #########
        # Outcome

        if Missed:
            logging.info("missed")
            datalog["missed"] = True
            scorer.scores["missed"] += 1
            totMissed += 1

            # raise alarm if too many stimuli missed
            print(totMissed)
            if totMissed > CONF["task"]["maxMissed"]:
                # TODO: sound alarm
                Alarm.play()
                datalog["alarm!"] = mainClock.getTime()
                logging.warning("alarm sound!!!!!")

        else:
            # show result
            reactionTime = keys[0].rt
            logging.info('RT: %s', reactionTime)
            screen.show_result(reactionTime)
            core.wait(CONF["fixation"]["scoreTime"])

            # exit if asked
            quitExperimentIf(keys[0].name == 'q')

            # reset missed count
            totMissed = 0

            # save to memory
            datalog["rt"] = reactionTime
            datalog["response_key"] = keys[0].name

            if reactionTime > CONF["task"]["minTime"]:
                scorer.newRT(reactionTime)
                if Late:
                    datalog["late"] = True
                    scorer.scores["late"] += 1

        # save data to file
        datalog.flush()

    # Brief blank period to rest eyes and signal block change
    screen.show_cue(f"{block} / {totBlocks}", )
    logging.info('Starting block switch rest period')
    core.wait(CONF["fixation"]["restTime"])

###########
# Concluion

# End main experiment
screen.show_cue("DONE!")
core.wait(CONF["timing"]["cue"])

# Get data score


# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')
# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

logging.info('Finished')


quitExperimentIf(True)
