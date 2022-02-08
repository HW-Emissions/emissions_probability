
# Requires numpy, scipy, pandas and matplotlib
# Recommend to use either pip or conda to create a venv
# using requirements file


import matplotlib.ticker as mtick
import scipy as sp
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF
from plot import style, plt  # noqa: F401
from funcs import get_cumsum, load_from_XLS

'''
--- Define Datasets ---

name: Used Internally
label: Used for plot legend
style: a matplotlib line style ('-c' is a solid cyan line)
dist: either a tuple containing (filename, column name, sheet name (defaults to Sheet1))
      or a two parameter list of a lognormal distribution [mu, sigma]

'''
leak_rate_unit = 'kg/hr'
leak_dists = [
    {'name': 'bc_emis', 'label': 'BC (BCOGC, 2020)',
     'style': 'ob', 'dist': ('bc_emis.xlsx', 'emis')},
    {'name': 'clear_emis', 'label': 'Alberta (Clearstone, 2018)',
     'style': 'og', 'dist': ('clearstone.xlsx', 'emis')},
    {'name': 'fw_emis', 'label': 'Fort Worth (2011)',
     'style': 'or', 'dist': ('ERG_Cam_2011.xlsx', 'emis')},
    {'name': 'fayetteville', 'label': 'Fayetteville (Alvarez, 2018)',
     'style': '-b', 'dist': [-2.2, 2.4]},
    {'name': 'weld', 'label': 'Weld (Alvarez, 2018)',
     'style': '-g', 'dist': [-0.62, 1.2]},
    {'name': 'ZA_production', 'label': 'Barnett Production (Zavala-Araiza, 2015)',
     'style': '-r', 'dist': [-1.79, 2.17]},
    {'name': 'ZA_compressor', 'label': 'Barnett Compressor (Zavala-Araiza, 2015)',
     'style': '-m', 'dist': [3.05, 1.49]},
    {'name': 'ZA_processing', 'label': 'Barnett Processing (Zavala-Araiza, 2015)',
     'style': '-c', 'dist': [4.41, 1.31]},
]

# --- Load Data ---
for obj in leak_dists:
    if isinstance(obj['dist'], tuple):
        obj.update({'leaks': load_from_XLS(*obj['dist'])})
        cumsum, leaks = get_cumsum(leaks=obj['leaks'], decending = False)
        obj.update({'cumsum': cumsum, 'leaks': leaks})
    else:
        obj.update(
            {'fit_dist': sp.stats.lognorm(obj['dist'][1], loc=0, scale=np.exp(obj['dist'][0]))})
        cumsum, leaks = get_cumsum(dist=obj['fit_dist'], decending = False)
        obj.update({'cumsum': cumsum, 'leaks': leaks})


# --- Generate Plots ---
x = np.linspace(0.00001, 1000, 100000)
fig, ax = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
for obj in leak_dists:
    if 'o' in obj['style']:
        extra_style = {'markersize': 4, 'alpha': 0.7}
    else:
        extra_style = {'linewidth': 2, 'alpha': 0.7}
    ax.plot(obj['leaks'], obj['cumsum'], obj['style'],
            label='% of emis: {}'.format(obj['label']), **extra_style)
    if 'fit_dist' in obj:
        ax.plot(x, obj['fit_dist'].cdf(x), obj['style'].replace('-', '--'),
                label='% of leaks: {}'.format(obj['label']), **extra_style)
    else:
        ecdf = ECDF(obj['leaks'])
        ax.plot(ecdf.x, ecdf.y, obj['style'].replace('o', '*'),
                label='% of leaks: {}'.format(obj['label']), **extra_style)

# Set Axises
ax.set_xscale('log')
ax.legend()
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set(xlabel='Leak rate ({})'.format(leak_rate_unit), ylabel='CDF (%)')
ax.set_xlim(10 ** -2, 10 ** 4)
ax.xaxis.grid(True, which='minor', alpha=0.6)
ax.yaxis.grid(True, which='major', alpha=0.6)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.78))
plt.show()
xxx = 10
