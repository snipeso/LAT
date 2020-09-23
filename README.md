# Lateralized Attention Task (LAT)
A reaction time task designed to identify brief lapses in spatial attention. The task lasts 12 minutes. Two minutes at a time, one half of the visual field will be illuminated, and feint gray circles will appear randomly every 2-10 seconds, and shrink within .5s, and the participant has to press a button as fast as possible. If they respond before the circle disappears, it will flash green as feedback. If 5 consecutive stimuli are missed, a car horn will ring to wake up the participant.


## how to run

- in terminal write:
- `export participant=P00 session=1`
- `exp-LAT`

## Design

duration 16 min: 2 x 4 of each condition (for loop of list of conditions)
(for loop of blocks)

while block running, present circle with pos randomly determined
circle diameter gets reduced as a % of timer and total timer time, freezes and turns green if caught in time

## Todo

- fix visuals

### Eventual TODOs

- move session info to instructions

## How to make it executable

1. make sure there is the file exp-LAT
2. run `code ~/.bashrc` in terminal
3. add at the bottom: `export PATH=~/Projects/LAT/:$PATH`
4. give permission to use that file: `chmod +x Projects/LAT/exp-LAT`

Then from a new terminal, you can run directly `exp-LAT` and it starts!

## How to reproduce the env

- run `cp {env} .`
- run `pyvenv env`

## How to measure timing

1. Set the stimulus position to always be 0.0, and the color to be blue, and the ISI (inter stimulus interval) is between 1 and 2
2. on an iphone 6 or later (but better if less than XR), download the app "is it snappy"
3. start recording just before starting the task, such that the key you will press and the screen are both in view
4. play the task at least 20 trials
5. on the app, reveiw the video
   - go frame by frame until you reach the first frame in which the stimulus appears
   - mark this as "input" in the bottom left
   - continue until the first frame in which you visibily see the key being pressed down, mark this as "output"
     the app will calculate the difference in miliseconds. repeat until desired.
6. open the output, identify the corresponding reaction times, subtract, and determine the average difference between filmed RTs and computer recorded RTs

## Notes

unlike with countdown, less motivation to improve score
