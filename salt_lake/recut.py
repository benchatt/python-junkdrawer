def avg(lst):
    if len(lst) == 0:
        return 0
    return round(sum([float(x) for x in lst]) / float(len(lst)), 1)

def recut(data):
    goodkeys = ['level', 'TEMP', 'MAX', 'WDSP', 'PRCP', 'SNDP']
    result = []
    wndw = []
    for n in range(len(data)):
        thisrow = {k:float(data[n][k]) for k in goodkeys}
        if n == 0:
            thisrow['delta'] = 0.0
        else:
            thisrow['delta'] = round(thisrow['level'] - result[n-1]['level'],1)
        wndw.append(thisrow)
        if len(wndw) > 180:
            del(wndw[0])
        for k in [j for j in goodkeys if j == j.upper()]:
            thisrow[f'{k}_180'] = \
                 avg([row[k] for row in wndw if float(row[k]) != 999.9])
            thisrow[f'{k}_30'] = \
                 avg([row[k] for row in wndw[-30:] if float(row[k]) != 999.9])
            thisrow[f'{k}_180_SUM'] = \
                 round(sum([row[k] for row in wndw if float(row[k]) != 999.9]),1)
        result.append(thisrow)
    return result
