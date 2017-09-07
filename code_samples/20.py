from itertools import count

def simple_infinite_spawn(time_step, x_val):
    for value in count(1):
        time = time_step * value
        yield time, x_val