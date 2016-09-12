from joystick import joystick

BUTTON_DICT = {
    0: 'A', 1: 'B', 2: 'X', 3: 'Y', 4: 'L',
    5: 'R', 6: 'C', 7: 'S', 8: 'U', 9: 'D', }
DIRECTION_LIST = [
    (0, 'left', 'right'), (1, 'up', 'down'),
    (2, 'E', 'F'), (3, 'G', 'H'), (4, 'I', 'J') ]
HAT_LIST = [(0, 'M', 'N'), (1, 'O', 'P')]

js = joystick()

def key_down(key):
    print('%s is pressed' % key)
def key_up(key):
    print('%s is released' % key)
def registe_button(k, v):
    @js.button_register(k)
    def button_fn(motion):
        if motion == 'down':
            key_down(v)
        elif motion == 'up':
            key_up(v)
def registe_axis_or_hat(register, i, neg, pos):
    @register(i)
    def axis_fn(status):
        if status == 0:
            key_up(neg); key_up(pos)
        elif status == 1:
            key_down(pos)
        elif status == -1:
            key_down(neg)

for k, v in BUTTON_DICT.items(): registe_button(k, v)
for directionTuple in DIRECTION_LIST: registe_axis_or_hat(js.axis_register, *directionTuple)
for hatTuple in HAT_LIST: registe_axis_or_hat(js.hat_register, *hatTuple)

js.init()
js.start()
try:
    while 1: raw_input()
except:
    pass
js.stop()
