# Program for testing the big display using an array
# of 5*5 microbits.
# 
# This will simply light up one pixel at a time. Which
# pixel it is can be set by Pushing button A to modify 
# the X position within the array, or by pushing button
# B to modify the Y position.
#
# This information is transferred by encoding each
# brightness as a single byte and chaining them together,
# in the following order:
#    x0y0 x1y0 x2y0 x3y0 x4y0  (bytes  0 -  4)
#    x0y1 x1y1 x2y1 x3y1 x4y1  (bytes  5 -  9)
#    x0y2 x1y2 x2y2 x3y2 x4y2  (bytes 10 - 14)
#    x0y3 x1y3 x2y3 x3y3 x4y3  (bytes 15 - 19)
#    x0y4 x1y4 x2y4 x3y4 x4y4  (bytes 20 - 24)
#
# A valid message (displaying a bright dot in the center)
# would thus look like this:
#
# "0000005550059500555000000"


import microbit
import radio

radio.on()
radio.config(power=7)


class BigDisplay:

    def __init__(self):
        self.state = ["0"] * 25
        radio.on()
        radio.config(power=7)   # Set the power level to 7 (highest, default=0)

    def set_pixel(self, x, y, value):
        assert value >= 0
        assert value < 10

        assert x >= 0
        assert x < 5
        assert y >= 0
        assert y < 5

        self.state[x + y*5] = str(value)[0]

        self.send_update()

    def get_pixel(self, x, y):
        assert x >= 0
        assert x < 5
        assert y >= 0
        assert y < 5

        return int(self.state[x + y*5])

    def clear(self, send_update=True):
        self.state = ['0'] * 25
        if send_update:
            self.send_update()

    def show(self, image):
        if image != self.state:
            self.state = list(image)
            self.send_update()

    def send_update(self):
        msg = "%s" % "".join(self.state)
        radio.send_bytes(msg)


big_display = BigDisplay()
pos_x = 2
pos_y = 2

while True:
    changed = False
    if microbit.button_a.was_pressed():
        pos_x = (pos_x + 1) % 5
        changed = True

    if microbit.button_b.was_pressed():
        pos_y = (pos_y + 1) % 5
        changed = True

    if changed:
        microbit.display.clear()
        microbit.display.set_pixel(pos_x, pos_y, 9)

        big_display.clear(send_update=False)
        big_display.set_pixel(pos_x, pos_y, 9)