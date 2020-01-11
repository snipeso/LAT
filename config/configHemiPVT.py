from config.configSession import CONF

CONF.update({
    "task": {
        "name": "hemiPVT",
        "duration": 2 * 60,  # duration of a block, in seconds
        "blocks": 8,  # number of blocks, try to be even
        "minTime": .1,  # in seconds, min time to be considered a valid RT
        "maxTime": 1,  # over this, RT considered a lapse
        "warningTime": 5,  # in seconds, time before a tone plays to wake participant up TODO: make this happen 1s after x consecutive lapses
        "victoryColor": "green",
        "earlyColor": "yellow",
        "color": "grey",
        "maxRadius": .1,  # in norm units
    },
    "fixation": {
        "colorOff": "black",
        "colorOn": "white",
        "height": .1,
        "width": .2,
        "boxColor": "red",
        "errorFlash": 0.1,  # in seconds, how long to flash box if key pushed during delay
        "minDelay":  0.5,  # 2,  # in seconds, minimum delay between stimuli
        "maxDelay": 1,  # 10,  # maximum delay between stimuli
        "scoreTime": 0.5  # in seconds, time to show final score
    },
    "instructions": {
        "text": "One half of the screen will be illuminated. Pay attention to that half, while keeping your gaze on the red rectangle. When a circle appears, click the F key before it disappears. If you saw it but weren't fast enough, press the key anyway.",
        "startPrompt": "Press any key to start. Press q to quit."
    },
})
