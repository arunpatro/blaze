from multiprocessing import Pool
import requests
import numpy as np
import time
from matplotlib import pyplot as plt
# url = 'http://releases.ubuntu.com/16.04.2/SHA1SUMS'
url = 'http://releases.ubuntu.com/16.04.2/ubuntu-16.04.2-desktop-amd64.iso.zsync'

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
    while True:
        try:
            r = requests.get(url, proxies=proxies, headers=headers)
            break
        except Exception as e:
            continue
    # print 'Completed connection {}'.format(tup[0])
    return r.content

    # print hashlib.md5(open(full_path, 'rb').read()).hexdigest()

if __name__ == '__main__':
    s = [1, 2 ,5, 10, 20, 50, 100, 200, 500]
    ts = []
    for i in s:
        n = 10
        p = Pool(i)
        
        response = requests.head(url)
        length = int(response.headers.get('content-length'))
        ranges = getRanges((0,length-1), n)
        ranges =  list(enumerate(ranges))
        t  = time.time()
        out = p.map(unit, ranges)
        ts.append( time.time() - t )
        print i

    plt.figure()
    plt.plot(s, ts)
    plt.savefig('blaze.png')
    plt.show()

    out = reduce((lambda x, y: x + y), out)
    # truth = requests.get(url, proxies=proxies).content
    # print out == truth


    # r2 = requests.get(url, proxies=proxies, stream=True)
    # print list(r2.iter_content(chunk_size=length/n))
    # print len(list(r2.iter_content(chunk_size=length/n)))

    print 'Saving'
    with open(url.split('/')[-1], 'w') as f:
        f.write(out)
