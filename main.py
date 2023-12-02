import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

plt.style.use('dark_background')
figure(figsize=(16, 8), dpi=60)
plt.rcParams["figure.figsize"] = (18,5)

from fin_func import *
from os import listdir
from os.path import isfile, join
from pathlib import *
import pandas as pd

