""" This module measures time and RAM usage
for creating 100,000 random dummy entities.
"""

import os
import random
import time
from pathlib import Path
import sys
sys.path.append(
    str(Path('../rague').resolve())
)

import psutil
from tqdm import tqdm

from rague.components import Position
from rague.entities import Dummy
from rague.world import World

world = World()

start = time.time()
for i in tqdm(range(100000), total=100000):
    x, y = random.randint(0, 1000), random.randint(0, 1000)
    world.entities.add(
        Dummy(Position(x, y))
    )
end = time.time()

process = psutil.Process(os.getpid())
mem = process.memory_info()[0] / float(2 ** 20)

print("Time:\t{} sec\nMemory:\t{}MiB".format(end-start, mem))
