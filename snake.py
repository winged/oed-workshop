import microbit
import random
import radio



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

# Initialize: Decide whether using local display or "big display" mode
microbit.display.scroll("A: BIG, B: SMALL")
while True:
    if microbit.button_a.was_pressed()
        disp = BigDisplay()
        break
    elif microbit.button_b.was_pressed():
        disp = microbit.display
        break

# There's always a goodie somewhere. If the head reaches
# it, we get longer and faster.
goodie = None

# The tail contains a counter for each place where the head
# has been. We count it down each round, and if it reaches zero,
# we remove the item from the tail.
tail = {}
head = (2,2) # Start in the center
length = 1

direction = 1 # up, see below
speed = 1000

# each possible direction is a pair of x, y coordinates.
# When advancing, the numbers area dded to the head.
directions = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]

def turn_left():
    global direction
    direction = (direction + 1) % 4

def turn_right():
    global direction
    direction = (direction - 1) % 4

def new_head():
    move_x, move_y = directions[direction]
    return (head[0] + move_x, head[1] + move_y)

def position_goodie():
    ok = False
    while not ok:
       new_pos = (random.randint(0,4), random.randint(0,4))
       ok = new_pos not in tail and new_pos != head
    return new_pos

def restart(msg):
    global tail, head, length, direction, speed, goodie
    microbit.display.scroll(msg, delay=80)
    microbit.sleep(2000)
    # Re-initialize again, next round
    goodie = position_goodie()
    tail = {}
    head = (2,2)
    length = 1
    direction = 0
    speed = 1000

# Get ready
random.seed()
restart("GET READY")

while True:
    # don't go too fast, but become faster as we get longer
    microbit.sleep(speed - length * 5)

    # direction change detection. Note that you can cancel a
    # turn if you hit the other button fast enough. But you
    # cannot turn the other way if you've pressed the wrong
    # button.
    if microbit.button_a.was_pressed(): turn_left()
    if microbit.button_b.was_pressed(): turn_right()

    # advance snake. We add the head's position to the tail,
    # then calculate the new position for the head.
    tail[head] = length
    head = new_head()

    # Detect wall hits. Output message and restart if we
    # hit the wall.
    if head[0] < 0 or head[0] > 4:
        restart("YOU HIT A WALL! %d points" % length)
        continue
    if head[1] < 0 or head[1] > 4:
        restart("YOU HIT A WALL! %d points" % length)
        continue

    # Detect tail bite, same procedure as above.
    if head in tail:
        restart("TAIL BITE! %d points" % length)
        continue

    # Draw the snake
    disp.clear()
    disp.set_pixel(head[0], head[1], 8)
    for pos in tail.keys():
        # display tail bit
        disp.set_pixel(pos[0], pos[1], 7)

        # remove tail if counter reached 0
        tail[pos] -= 1
        if tail[pos] <= 0:
            del tail[pos]

    # Something to eat?
    if head == goodie:
        length += 1
        goodie = position_goodie()
    # draw goodie
    disp.set_pixel(goodie[0], goodie[1], 9)
