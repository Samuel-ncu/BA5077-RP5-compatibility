import json
from urllib.request import Request, urlopen

base = 'http://127.0.0.1:11434'
model = 'smollm2:135m-instruct-q4_0'

def list_models():
    with urlopen(base + '/api/tags', timeout=30) as response:
        return json.load(response)['models']

before = list_models()
print('existing models:', [item['name'] for item in before], flush=True)
if any(item['name'] == model for item in before):
    print('already available:', model, flush=True)
else:
    print('downloading:', model, flush=True)
    payload = json.dumps({'model': model, 'stream': False}).encode('utf-8')
    request = Request(base + '/api/pull', data=payload,
                      headers={'Content-Type': 'application/json'}, method='POST')
    with urlopen(request, timeout=600) as response:
        result = json.load(response)
    print('pull status:', result['status'], flush=True)
    if result['status'] != 'success':
        raise RuntimeError('模型下載未完成')

after = list_models()
found = next((item for item in after if item['name'] == model), None)
if found is None:
    raise RuntimeError('下載後沒有在模型清單中找到模型')
print('model:', found['name'])
print('size bytes:', found['size'])
print('digest:', found['digest'])
