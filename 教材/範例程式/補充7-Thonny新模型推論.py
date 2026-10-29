import json
from urllib.request import Request, urlopen

model = 'smollm2:135m-instruct-q4_0'
payload = {
    'model': model,
    'prompt': 'In one short sentence, what does a temperature sensor measure?',
    'stream': False,
    'keep_alive': 0,
    'options': {'temperature': 0, 'num_predict': 60},
}
request = Request('http://127.0.0.1:11434/api/generate',
                  data=json.dumps(payload).encode('utf-8'),
                  headers={'Content-Type': 'application/json'}, method='POST')
print('asking model:', model, flush=True)
with urlopen(request, timeout=180) as response:
    result = json.load(response)
print('model:', result['model'])
print('response:', result['response'].strip())
print('done:', result['done'])
print('done reason:', result.get('done_reason'))
print('generated tokens:', result.get('eval_count'))
print('total seconds:', round(result['total_duration'] / 1_000_000_000, 2))
