import json
from urllib.request import Request, urlopen

request_data = {
    'model': 'tinyllama:latest',
    'prompt': 'In one sentence, what does an IoT temperature sensor measure?',
    'stream': False,
    'keep_alive': 0,
    'options': {'temperature': 0, 'num_predict': 40},
}
request = Request('http://127.0.0.1:11434/api/generate',
                  data=json.dumps(request_data).encode('utf-8'),
                  headers={'Content-Type': 'application/json'}, method='POST')
with urlopen(request, timeout=120) as response:
    result = json.load(response)
print('model:', result['model'])
print('response:', result['response'].strip())
print('done:', result['done'])
print('generated tokens:', result.get('eval_count'))
