# Name: kinspy
# Describes: provide convenient functions and constants
# Version: v1.0.6
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

def read_2columns(fp,i,j,is_csv = False):
    a_list = []
    b_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
    return np.array(a_list),np.array(b_list)

def read_3columns(fp,i,j,k,is_csv = False):
    a_list = []
    b_list = []
    c_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
        c_list.append(float(line_list[k]))
    return np.array(a_list),np.array(b_list),np.array(c_list)

