from multiprocessing import Pool
import requests
import numpy as np
import time
url = 'http://releases.ubuntu.com/16.04.2/SHA1SUMS'
# url = 'http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-server-amd64.template'

proxies = {
  'http': 'http://10.3.100.207:8080',
  'https': 'http://10.3.100.207:8080',
}

def getRanges(bytesRange, n):
    stepSize = (bytesRange[1] - bytesRange[0])/ n
    steps =  np.array([i * stepSize for i in range(n+1)])
    steps[-1] = steps[-1] + length % n 
    return zip(steps[:-1], (steps - 1)[1:])

def unit(tup):
    headers={'Range': 'bytes={}-{}'.format(tup[1][0], tup[1][1])}
    r = requests.get(url, proxies=proxies, headers=headers)
    print 'Completed connection {}'.format(tup[0])
    return r.content

def verify(hash1, hash2):
    return hash1==hash2
    # print hashlib.md5(open(full_path, 'rb').read()).hexdigest()


if __name__ == '__main__':
    n = 10
    p = Pool(n)
    
    response = requests.head(url)
    length = int(response.headers.get('content-length'))
    ranges = getRanges((0,length-1), n)
    t  = time.time()
    ranges =  list(enumerate(ranges))
    out = p.map(unit, ranges)
    print time.time() - t
    out = reduce((lambda x, y: x + y), out)
    truth = requests.get(url, proxies=proxies).content
    print verify(out, truth)

    with open(url.split('/')[-1], 'w') as f:
        f.write(out)

