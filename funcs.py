from numpy import cumsum, array
from pandas import ExcelFile


def get_cumsum(leaks=None, dist=None,  size=100000, decending = True):
    if leaks is None:
        leaks = dist.rvs(size=100000)
    leaks.sort()
    if decending:
        leaks = leaks[::-1]
    return cumsum(leaks)/sum(leaks), leaks


def load_from_XLS(file, column, sheet='Sheet1'):
    prog_file = ExcelFile(file)
    data = prog_file.parse(sheet)
    return array(data[column])
