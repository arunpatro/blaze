import requests
url = 'http://releases.ubuntu.com/16.04.2/SHA1SUMS'

proxies = {
  'http': 'http://10.3.100.207:8080',
  'https': 'http://10.3.100.207:8080',
}

headers = {}

response = requests.head(url)
content = int(response.headers.get('content-length'))
steps = [int(content/2), content - int(content/2)]

headers={'Range': 'bytes=0-220'}
r = requests.get(url, proxies=proxies, headers=headers)
print r.content, type(r.content), len(bytearray(r.content, 'utf-8'))

headers={'Range': 'bytes=221-443'}
r2 = requests.get(url, proxies=proxies, headers=headers)
print r2.content, type(r2.content), len(bytearray(r2.content, 'utf-8'))

with open('SHA1SUMS_','w') as f:
	f.write(r.content + r2.content)


