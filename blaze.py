import multiprocessing
from multiprocessing import Pool
import requests
import time
from math import ceil
import os
import psutil
from matplotlib import pyplot as plt
import numpy as np

# url = 'http://releases.ubuntu.com/16.04.2/SHA1SUMS'
# url = 'http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-server-i386.jigdo'
# url = 'http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-server-i386.iso.zsync'
url = 'http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-server-i386.template'
proxies = {
  'http': 'http://10.3.100.207:8080',
  'https': 'http://10.3.100.207:8080',
}

def getRanges(bytesRange, n):
    stepSize = (bytesRange[1] - bytesRange[0])/ n
    steps =  np.array([i * stepSize for i in range(n+1)])
    steps[-1] = steps[-1] + (bytesRange[1] - bytesRange[0]) % n 
    return zip(steps[:-1], (steps - 1)[1:])

def unit(tup):
    headers={'Range': 'bytes={}-{}'.format(tup[1][0], tup[1][1])}
    l = tup[1][1] - tup[1][0] + 1
    while True:
        try:
            r = requests.get(url, stream=True, proxies=proxies, headers=headers)
            break
        except Exception as e:
            print 'Connection Error. Attempting again {}'.format(tup[0])
            continue
    # content = str()
    # for i in r.iter_content(chunk_size=10):
        # content += i
        # bar.update(len(content)*100.0/l)
    # print 'Completed connection {}'.format(tup[0]), os.getppid(), os.getpid()
    return r.content


def main(url, n):
    p = Pool(n)
    response = requests.head(url)
    length = int(response.headers.get('content-length'))
    # print 'Downloading {} {} bytes'.format(url, length)
    ranges = getRanges((0,length), n)
    ranges =  list(enumerate(ranges))
    t  = time.time()
    out = p.map(unit, ranges)
    p.close()
    p.join()
    t = time.time() - t
    print t
    return reduce((lambda x, y: x + y), out), t

def self(x):
    # print os.getppid(), os.getpid()
    return x
    
def parallelChunk(url, n):
    p = Pool(n)
    response = requests.head(url)
    length = int(response.headers.get('content-length'))
    chunkSize = length/n
    # print 'Downloading {} {} bytes'.format(url, length)
    r = requests.get(url, stream=True, proxies=proxies)
    points = r.iter_content(chunk_size=chunkSize)
    t = time.time()
    out = p.map(self, points)
    p.close()
    p.join()
    t = time.time() - t
    print t
    return reduce((lambda x, y: x + y), out), t

if __name__ == '__main__':
    t1 = []
    t2 = []
    times = 5
    for i in 10*(np.arange(times) + 1):
        print i
        t1.append(np.mean([parallelChunk(url, i)[-1] for _ in range(10)]))
        t2.append(np.mean([main(url, i)[-1] for _ in range(10)]))
    plt.figure()
    plt.plot(10*(np.arange(times) + 1), t1, 'r.-', 10*(np.arange(times) + 1), t2, 'b.-')
    plt.savefig('out.png')
    # truth = requests.get(url, proxies=proxies).content
    # print truth = main(url, 5)
    # print truth == parallelChunk(url, 5)[0]
    # print hashlib.md5(open(full_path, 'rb').read()).hexdigest()

    # print 'Saving'
    # with open(url.split('/')[-1], 'w') as f:
        # f.write(content)
    