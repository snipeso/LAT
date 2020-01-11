CONF = {
    "participant": "01",
    "session": "1",
    "screen": {
        "full": False,
        "color": "#6B6B6B",
        "monitor": 'Extreme',  # "testMonitor",
        # screen size when not fullscreen TODO: rename to windows size
        "debugResolution":  [1000, 1000],  # [384, 216],
        "debugSize": [10, 10],
        "units": "norm",
        "resolution": [3840, 2160],
        # Obtain from xrandr in command window TODO: rename to size
        "size": [34.4, 19.3]
    },
    "timing": {
        "rest":  1,  # 60,
        "overview": 1,
        "cue": 1
    },
    "showInstructions": True,
}
