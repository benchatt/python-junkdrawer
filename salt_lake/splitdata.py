import numpy as np

def splitdata(data):
    #xkeys = [k for k in data[0].keys() if k == k.upper() and '_' not in k]
    #xkeys.extend(['level','timestamp','date'])
    xkeys = data[0].keys()
    trainx = []
    trainy = []
    testx = []
    testy = []
    for n in range(len(data)):
        thisx = []
        for key in xkeys:
            if key == 'delta':
                continue
            if key == 'FRSHTT' or key == 'date':
                thisx.append(int(data[n][key]))
            else:
                thisx.append(float(data[n][key]))
        thisy = data[n]['delta']
        if n % 5 == 4:
            testx.append(thisx)
            testy.append(thisy)
        else:
            trainx.append(thisx)
            trainy.append(thisy)
    return {'train_X': np.array(trainx),
            'train_y': np.array(trainy),
            'test_X': np.array(testx),
            'test_y': np.array(testy)}
