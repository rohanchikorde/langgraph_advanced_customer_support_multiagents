import sys
from pathlib import Path
# Add project root to path so 'src' package can be imported when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)
resp = client.post('/api/v1/support/query', json={'query':'hi','user_id':'test_user_hi'})
print('Status code:', resp.status_code)
print('Response JSON:', resp.json())
if resp.status_code==200:
    body = resp.json()
    if '12345' in body.get('response',''):
        print('❌ Fix failed: response contains 12345')
    else:
        print('✅ Fix passed: greeting response is generic/no order id')
else:
    print('❌ API returned error')
