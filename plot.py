
import pandas as pd
from numpy import array
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
import scipy as sp
import numpy as np
import seaborn as sns
import matplotlib.style as style

style.use('seaborn-colorblind')
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 16
mpl.rcParams['font.family'] = 'Arial'
sns.set_style("whitegrid")
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
