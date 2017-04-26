# A micro:bit battleships implementation.
# Each micro:bit is a battleship with a randomly chosen location.
# At random intervals, a bomb is sent out to the other partaking
# microbits. If a bomb hits the location of another microbit, it
# will die.
import radio
import random
from microbit import accelerometer, display, sleep, Image, button_a
import music


# The radio won't work unless it's switched on.
radio.on()

flash = [Image().invert()*(i/9) for i in range(9, -1, -1)]
IDENTITY = (random.randint(0, 4), random.randint(0, 4))
DEAD     = False

kills = set()

def update_display():
    global kills
    if DEAD:
        display.show(Image.SAD)
        return

    display.set_pixel(IDENTITY[0], IDENTITY[1], 9)

    new_kills = set()
    for x,y,val in kills:
        display.set_pixel(x,y,val)
        if val > 0:
            new_kills.add((x, y, val-1))
    kills = new_kills


def parse_msg(msg):
    x = int(msg[0], 10)
    y = int(msg[1], 10)
    kills.add((x,y,8))

    if (x,y) == IDENTITY:
        die()


def die():
    global DEAD
    display.show(flash, delay=200, wait=False)
    music.play(music.POWER_DOWN)
    # Dying animation
    DEAD = True


def send_bomb():
    "Send a bomb to a random location (hope it's not us...)"
    x, y = (random.randint(0, 4), random.randint(0, 4))

    music.play(music.BA_DING)

    radio.send('%d%d' % (x, y))


def zombie():
    # Become mass murdering zombie
    display.show(Image.ANGRY)
    music.play(music.NYAN, wait=False)
    for x in range(0, 5):
        for y in range(0, 5):
            radio.send('%d%d' % (x, y))
            sleep(600)

def alive():

    # Event loop.
    while not DEAD:
        update_display()
        incoming = radio.receive()
        if incoming is not None and len(incoming) == 2:
            # bomb dropped!
            parse_msg(incoming)
        sleep(100)

        if button_a.was_pressed() or random.randint(0, 100) == 0:
            send_bomb()

while True:
    # be alive...
    alive()

    # Die
    update_display()

    # Become a zombie maybe?
    if random.randint(0, 10) == 0:
        zombie()


    # be dead for 10s, then start again (good zombie?)
    sleep(10000)
    display.clear()
    music.play(music.PRELUDE)
    DEAD = False
    # ignore what has happened while we were dead
    while radio.receive() is not None:
        pass
