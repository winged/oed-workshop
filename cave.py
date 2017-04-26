# Navigate the cave by using the gravity / acceleration sensor

import random
import microbit

MAX_SPEED = 0.8
MIN_SPEED = -1.0

gravity = 0.02
jump_strength = 0.2
vspeed = 0
position = 2.0
last_proc = microbit.running_time()
speed = 0.16
max_obstacles = 5
start_time = microbit.running_time()

map_position = 0.0
pos_acc = 0

obstacles = set()
display_buffer = set()


def reset(msg):
    global position, last_proc, speed, map_position, obstacles, vspeed
    global max_obstacles, start_time
    obstacles = set()
    map_position = 0
    speed = 1.0
    vspeed = 0
    position = 2
    last_proc = microbit.running_time()
    microbit.display.scroll(msg)
    microbit.sleep(1000)
    max_obstacles = 5
    start_time = microbit.running_time()


def check_alive():
    # if position < 0:
    #     reset("You crashed into the floor!")
    # elif position >= 5.0:
    #     reset("You crashed into the ceiling!")
    if (int(map_position), int(position)) in obstacles:
        reset("You hit an obstacle!")
    else:
        return True
    return False


def move_pilot():
    global position
    position += vspeed
    position = min(position, 4)
    position = max(position, 0)


def pos_from_accelerometer():
    global position, pos_acc
    position = microbit.accelerometer.get_z() / 160.0 - pos_acc
    if position < 0:
        pos_acc += position
        position = 0
    elif position > 4:
        pos_acc += position - 4.0
        position = 4.0


def update_speed(delta_t):
    global vspeed
    vspeed += gravity * float(delta_t) / 120.0
    vspeed = min(vspeed, MAX_SPEED)
    vspeed = max(vspeed, MIN_SPEED)


def check_button(delta_t):
    global vspeed
    if microbit.button_a.was_pressed():
        vspeed -= jump_strength * float(delta_t) / 120.0


def vspeed_from_accelerometer():
    global vspeed
    vspeed = microbit.accelerometer.get_z() / 800.0


def place_obstacles():
    global max_obstacles
    if len(obstacles) < max_obstacles:
        offs = int(map_position)+5
        obs = (random.randint(offs, offs+10), random.randint(0, 4))
        obstacles.add(obs)

    game_time = microbit.running_time() - start_time

    # every 5 seconds, add an obstacle
    max_obstacles = int(5 + game_time / 1000.0 / 5.0)


def evolve():
    global obstacles, map_position, position, last_proc, vspeed

    delta_t = (microbit.running_time() - last_proc)
    place_obstacles()
    # check_button(delta_t)
    # update_speed(delta_t)
    # vspeed_from_accelerometer()
    pos_from_accelerometer()

    # move_pilot()

    # if we hit ceiling or the floor, reset the speed to 0
    if position in (0, 4):
        vspeed = 0
    map_position += delta_t * speed / 100

    last_proc += delta_t


def draw():
    # Make a buffer, so we don't redraw if we don't need to.
    # This keeps the display from flickering.
    global display_buffer
    new_buffer = set()
    new_buffer.add((0, int(position), 9,))  # "pilot"
    for x, y in obstacles:
        if x < map_position or x > map_position + 4:
            continue
        new_buffer.add((int(x - map_position), y, 6,))

    if new_buffer != display_buffer:
        microbit.display.clear()
        for arg in display_buffer:
            microbit.display.set_pixel(*arg)
        display_buffer = new_buffer


def cleanup():
    global obstacles
    obstacles = set([
        (x, y)
        for (x, y) in obstacles
        if x > map_position
    ])


while True:
    evolve()
    if not check_alive():
        continue
    draw()
    microbit.sleep(50)
    cleanup()
