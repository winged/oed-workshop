Open Education Day 29. 04. 2017 - Code samples
==============================================

This contains the following programs for the micro:bit:

* *compass.py* - A very simple compass. Uses the clock predefined images to
  point towards north
* *cave.py* - Navigate a cave by tilting the device

* *battleships.py* - Two devices represent ships at random positions on the
  field, sending bombs to random places. If they're hit, it's game over.

* *Big Display*: Program to use 25 microbits to represent the 5x5 display.

  - *bigdisplay_pixel.py* - The program to run on the "pixel" devices. Push
    buttons A and B to select which pixel to represent.
  - *bigdisplay_test.py* - Test script for the big display. Buttons A and B
    can be used to light up a single pixel at a time.

* *snake.py* - The classic Nokia Snake. Buttons A and B turn the snake left and
  right. This version is modified to be able to use the big display code above.

* *firefly.py* - Firefly simulation. Upon a button press, the firefly lights up
  and sends a signal to other fireflies. Those will respond randomly, repeating
  the cycle.
