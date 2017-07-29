from multiprocessing import Pool
import requests
import numpy as np
from math import floor
url = 'http://releases.ubuntu.com/16.04.2/SHA1SUMS'

proxies = {
  'http': 'http://10.3.100.207:8080',
  'https': 'http://10.3.100.207:8080',
}

def getRanges(bytesRange, n):
    stepSize = (bytesRange[1] - bytesRange[0])/ n
    steps =  np.array([i * stepSize for i in range(n+1)])
    steps[-1] = steps[-1] + length % n 
    return zip(steps[:-1], (steps - 1)[1:])

def unit(range):
    headers={'Range': 'bytes={}-{}'.format(range[0], range[1])}
    r = requests.get(url, proxies=proxies, headers=headers)
    return r.content

def verify(hash1, hash2):
    print hash1==hash2

if __name__ == '__main__':
    n = 4
    p = Pool(n)
    
    response = requests.head(url)
    length = int(response.headers.get('content-length'))
    ranges = getRanges((0,length-1), n)
    out = p.map(unit, ranges)
    out = reduce((lambda x, y: x + y), out)
    truth = requests.get(url, proxies=proxies).content
    verify(out, truth)





