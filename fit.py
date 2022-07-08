

import numpy as np
from scipy.optimize import curve_fit

def log_fit( x, mu, sigma ):
    return 1 / x * 1. / (sigma * np.sqrt( 2. * np.pi ) ) * np.exp( -( np.log( x ) - mu )**2 / ( 2. * sigma**2 ) )

def get_bin_center(bins):
    centers = []
    for cnt, _ in enumerate(bins):
        if cnt < len(bins)-1:
            centers.append((bins[cnt+ 1] + bins[cnt])/2)
    return centers

def log_fit_scotts(data):
    logged_results = np.log(data)
    max_log_emis, min_log_emis = np.max(logged_results), np.min(logged_results)
    # std_log_emis = np.std(logged_results)
    # bw = 3.49*std_log_emis/(len(data)**(1/3)) # Scotts Method
    # n_bins = int(np.ceil((max_log_emis - min_log_emis)/ bw))
    logged_bins = np.linspace(min_log_emis, max_log_emis, num=80)
    bins = np.exp(logged_bins)
    bin_centers = get_bin_center(bins)
    hist, _ = np.histogram(data, bins=bins, density=True)
    mu_sig, err = curve_fit(log_fit, bin_centers, hist)
    return mu_sig[0], mu_sig[1]