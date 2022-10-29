import numpy as np

class AxisChunk:
    def __init__(self):
        self.x = None
        self.y = None

class DataChunk:
    def __init__(self):
        self.train = AxisChunk()
        self.test = AxisChunk()
        self.predict = AxisChunk()

def normsplit(data, fake, normer):
    finallevel = data[-1]['level']
    for n in range(len(fake)):
        fake[n]['level'] = finallevel
    alldata = data + fake
    big_y = []
    keys = list(alldata[0].keys())
    keys.remove('delta')
    for n in range(len(alldata)):
        if n < len(data):
            big_y.append(alldata[n]['delta'])
        alldata[n] = [float(alldata[n][k]) for k in keys]
    alldata = normer(np.array(alldata))
    output = DataChunk()
    output.predict.x = alldata[len(data)+1:]
    output.train.x = [alldata[i] for i in range(len(data)) if i % 5 != 4]
    output.test.x = [alldata[i] for i in range(len(data)) if i % 5 == 4]
    output.train.y = [big_y[i] for i in range(len(data)) if i % 5 != 4]
    output.test.y = [big_y[i] for i in range(len(data)) if i % 5 == 4]
    return output
