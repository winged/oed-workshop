# Program for running a big display using an array
# of 5*5 microbits.
#
# Pushing button A will modify the X position within
# the array, button B will modify the Y position.
#
# There is a single master device that will send out
# information on which pixels to be active. This information
# is transferred by encoding each brightness as a single
# byte and chaining them together, in the following order:
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
radio.config(power=6)

microbit.display.show(microbit.Image("00000:05550:05950:05550:00000:"))

pos_x = 2
pos_y = 2

while True:
    if microbit.button_a.was_pressed():
        pos_x = (pos_x + 1) % 5
        microbit.display.clear()
        microbit.display.set_pixel(pos_x, pos_y, 9)

    if microbit.button_b.was_pressed():
        pos_y = (pos_y + 1) % 5
        microbit.display.clear()
        microbit.display.set_pixel(pos_x, pos_y, 9)

    try:
        msg = radio.receive_bytes()
    except ValueError:
        # Not sure why this is needed - happens
        # some times
        msg = None

    if msg is not None:
        print(msg)

        offset = pos_x + pos_y*5
        try:
            value = int(msg[offset])
            microbit.display.show(microbit.Image()*value)
        except ValueError:
            print(msg)
        except IndexError:
            print(msg)
            print("")
            n = 5
            for i in range(0, len(msg), n):
                print(msg[i:i+n])
