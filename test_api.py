import urllib.request
import urllib.error
import json
import time

time.sleep(2)

# 1. Check health
r = urllib.request.urlopen('http://127.0.0.1:5003/health')
health = json.loads(r.read())
print('=== HEALTH CHECK ===')
print('Status:', health['status'])
print('API Configured:', health['api_configured'])
print('Message:', health['message'])
print()

# 2. Test real YouTube search
print('=== LIVE YOUTUBE SEARCH TEST ===')
payload = json.dumps({'keyword': 'artificial intelligence', 'count': 3}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:5003/fetch_videos/',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print('Got', len(data), 'videos!')
    for i, v in enumerate(data, 1):
        title = v['title'][:60]
        sentiment = v['sentiment']
        polarity = v['polarity']
        channel = v['channel']
        print(str(i) + '. [' + sentiment + '] ' + title)
        print('   Polarity: ' + str(polarity) + ' | Channel: ' + channel)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print('ERROR:', body)
