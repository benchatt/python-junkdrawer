from datetime import datetime
from random import sample

def avg(lst):
    return round(sum(lst) / float(len(lst)),1)

def gendata(data, accept):
    result = []
    simplekeys = [k for k in data[0].keys() if k == k.upper() and '_' not in k]
    #yesterday = float(data[-1]['timestamp']) * 100
    for n in range(9200):
        thisrow = {}
        #today = yesterday + 86400
        # ^^ seconds in a day
        #thisrow['timestamp'] = str(int(today / 100))
        #todayobj = datetime.fromtimestamp(today)
        #monthday = f'{todayobj.month:02}{todayobj.day:02}'
        #if monthday == '0229':
        #    monthday = '0228'
        #thisrow['date'] = monthday
        oneeighty = []
        if n > 179:
            oneeighty = result[n-180:]
        else:
            oneeighty.extend(result)
            oneeighty.extend(data[0-(180-n):])
        thirty = oneeighty[-30:]
        for k in simplekeys:
            thisrow[k] = sample(accept[monthday][k],1)[0]
            thisrow[f'{k}_180'] = avg([float(row[k]) for row in oneeighty])
            thisrow[f'{k}_30'] = avg([float(row[k]) for row in thirty])
            thisrow[f'{k}_180_SUM'] = \
                    sum([float(row[k]) for row in oneeighty])
        result.append(thisrow)
    return result
