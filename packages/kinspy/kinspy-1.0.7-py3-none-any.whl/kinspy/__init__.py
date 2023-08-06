# Name: kinspy
# Describes: provide convenient functions and constants
# Version: v1.0.7
# Date: 2021-12-16
# Author: Yunxiao Zhang
# E-mail: yunxiao9277@gmail.com

# imports
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import torch as t

# common functions
from numpy import sqrt, sin, cos, exp, log

# common constants
from numpy import pi, e

# file functions
def skip_nlines(fp,n):
    for i in range(n): fp.readline()

import numpy as np

def read_columns(fp,*index,sep = " "):
    y = [[] for i in index]

    for line in fp:
        for i in index:
            y[i].append(float(line.strip().split(sep)[i]))
    return (np.array(y[i]) for i in index)
