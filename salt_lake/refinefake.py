from datetime import datetime, timedelta

def avg(lst):
    if len(lst) == 0:
        return 0
    return round(sum([float(x) for x in lst]) / float(len(lst)), 1)

def refinefake(fake, data):
    goodkeys = ['TEMP', 'MAX', 'WDSP', 'PRCP', 'SNDP']
    result = []
    back180 = data[-180:]
    for i,row in enumerate(fake):
        thisrow = {k:row[k] for k in goodkeys}
        this180 = []
        if i < 179:
            this180.extend(back180[i-180:])
            this180.extend(result)
        else:
            this180.extend(result[i-180:])
        this30 = this180[-30:]
        for k in goodkeys:
            key180 = [r[k] for r in this180]
            key30 = [r[k] for r in this30]
            thisrow[f'{k}_180'] = \
                    round(avg([float(x) for x in key180 if float(x) != 999.9]),1)
            thisrow[f'{k}_30'] = \
                    round(avg([float(x) for x in key30 if float(x) != 999.9]),1)
            thisrow[f'{k}_180_SUM'] = \
                    round(sum([float(x) for x in key180 if float(x) != 999.9]),1)
        result.append(thisrow)
    return result
