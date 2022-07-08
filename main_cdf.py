
# Requires numpy, scipy, pandas and matplotlib
# Recommend to use either pip or conda to create a venv
# using requirements file


import matplotlib.ticker as mtick
import scipy as sp
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF
from plot import style, plt  # noqa: F401
from funcs import get_cumsum, load_from_XLS

# --- User Inputs ---

leak_rate_unit = 'kg/hr'
fit_distribution = "lognorm"
# scypi distribution types
# ie : lognorm, fatiguelife, alpha, chi2, genpareto
x = np.linspace(0.00001, 100, 100000)
leak_dists = [
    {'name': 'bc_emis', 'label': 'BC (BCOGC, 2020)',
     'style': '-b', 'dist': ('bc_emis.xlsx', 'emis'),
     'extra_style':{}},
    {'name': 'clear_emis', 'label': 'Alberta (Clearstone, 2018)',
     'style': '-g', 'dist': ('clearstone.xlsx', 'emis'),
     'extra_style':{}},
    {'name': 'fw_emis', 'label': 'Fort Worth (2011)',
     'style': '-r', 'dist': ('ERG_Cam_2011.xlsx', 'emis'),
     'extra_style':{}},
]


# --- Load Data ---
for obj in leak_dists:
    obj.update({'leaks': load_from_XLS(*obj['dist'])})
    ecumsum, _ = get_cumsum(leaks=obj['leaks'], decending = False)
    dist = getattr(sp.stats, fit_distribution)
    params = dist.fit(obj['leaks'], floc=0)
    dist = dist(params[:-2], params[-2], scale=params[-1])
    if fit_distribution == 'lognorm':
      print("{}: {} has parameters mu={}, sigma={}".format(
          obj['name'], 
          fit_distribution,  
          np.around(np.log(params[-1]), 3), 
          np.around(params[0], 3)
      ))
    else:
      print("{}: {} has parameters scale={}, shape={}".format(
          obj['name'], 
          fit_distribution,  
          np.around(params[-1], 3), 
          np.around(params[:-2], 3)
      ))

    fcumsum, fleaks = get_cumsum(dist=dist, decending = False)
    obj.update(
      {'ecumsum': ecumsum, 
        'eleaks': obj['leaks'], 
        'fcumsum': fcumsum,
        'fleaks': fleaks,
        'dist_params':(params)
    })

# --- Generate Plots ---
fig, ax = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
for obj in leak_dists:
    ax.plot(obj['leaks'], obj['ecumsum'], obj['style'],
            label='Emp. % of emis: {}'.format(obj['label']),linewidth=2)
    ecdf = ECDF(obj['eleaks'])
    ax.plot(ecdf.x, ecdf.y, obj['style'].replace('-', '--'),
            label='Emp. % of leaks: {}'.format(obj['label']),linewidth=2)
    ax.plot(obj['fleaks'], obj['fcumsum'], obj['style'].replace('-', '-.'),
            label='Fit % of emis: {}'.format(obj['label']),**obj['extra_style'])
    fecdf = ECDF(obj['fleaks'])
    ax.plot(fecdf.x, fecdf.y, obj['style'].replace('-', ':'),
            label='Fit % of leaks: {}'.format(obj['label']),**obj['extra_style'])

# Set Axises
ax.set_xscale('log')
ax.legend()
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set(xlabel='Leak rate ({})'.format(leak_rate_unit), ylabel='CDF (%)')
ax.set_xlim(10 ** -3, 10 ** 2)
ax.xaxis.grid(True, which='minor', alpha=0.6)
ax.yaxis.grid(True, which='major', alpha=0.6)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.78))
plt.show()
xxx = 10
