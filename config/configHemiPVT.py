from config.configSession import CONF

CONF.update({
    "task": {
        "name": "hemiPVT",
        "duration": 2*80,  # 2 * 60,  # duration of a block, in seconds
        "blocks": 4,  # number of blocks, try to be even
        "minTime": .1,  # in seconds, min time to be considered a valid RT
        "maxTime": .5,  # over this, RT considered a lapse
        # time window after stimulus disappearance when it still counts as a key response
        "extraTime": .5,
        "victoryColor": "green",
        "earlyColor": "yellow",
        "color": '#F7F7F7',
        "maxRadius": 2,  # in cm of screen width
        "maxMissed": 3
    },
    "fixation": {
        "colorOff": "black",
        "colorOn": "white",
        "height": .1,
        "width": .2,
        "boxColor": "red",
        "errorFlash": 0.1,  # in seconds, how long to flash box if key pushed during delay
        "minDelay":  2,  # 1   # in seconds, minimum delay between stimuli. these values compensate for other delays introduced in the process
        "maxDelay": 10,  # 10,  # 10,  # maximum delay between stimuli
        "scoreTime": 0.5,  # in seconds, time to show final score
        "restTime": 2,
    },
    "instructions": {
        "text": "One half of the screen will be illuminated. Pay attention to that half, while keeping your gaze on the red rectangle. When a circle appears, click the F key before it disappears. If you saw it but weren't fast enough, press the key anyway.",
        "startPrompt": "Press any key to start. Press q to quit."
    },
    "tones": {
        "minTime": 2,
        "maxTime": 5,
        "alarm": "horn.wav",
        "tone": "Pink50ms.wav",
        "volume": 0.3  # TODO: get volume to 55 db? need to test
    }
})


CONF["screen"]["size"] = CONF["screen"]["size"] if CONF["screen"]["full"] else CONF["screen"]["debugSize"]
CONF["screen"]["resolution"] = CONF["screen"]["resolution"] if CONF["screen"]["full"] else CONF["screen"]["debugResolution"]
