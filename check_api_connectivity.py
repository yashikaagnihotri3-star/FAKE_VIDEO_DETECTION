import requests, sys
url = 'https://api.realitydefender.ai/v1/detect'
print('Testing connectivity to', url)
try:
    r = requests.get('https://api.realitydefender.ai/')
    print('GET https://api.realitydefender.ai/ status:', r.status_code)
except Exception as e:
    print('GET request failed:', type(e).__name__, str(e))

try:
    # send a small HEAD/OPTIONS to check host reachability
    r2 = requests.options(url, timeout=10)
    print('OPTIONS status:', r2.status_code)
    print('Headers:', r2.headers.get('Allow'))
except Exception as e:
    print('OPTIONS/HEAD failed:', type(e).__name__, str(e))

# Also try DNS resolution via socket
import socket
host = 'api.realitydefender.ai'
try:
    addr = socket.gethostbyname(host)
    print('Resolved', host, 'to', addr)
except Exception as e:
    print('DNS resolution failed:', type(e).__name__, str(e))

# Quick POST with no file (should probably 4xx/405) — shows connection
try:
    r3 = requests.post(url, headers={'x-api-key': 'test'}, timeout=10)
    print('POST status:', r3.status_code)
    print('Response text (truncated):', (r3.text or '')[:500])
except Exception as e:
    print('POST failed:', type(e).__name__, str(e))

print('\nDone')
