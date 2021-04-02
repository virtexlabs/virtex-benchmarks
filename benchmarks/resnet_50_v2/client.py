import os
import pprint
from glob import glob

import numpy as np

from virtex import HttpMessage, HttpLoadTest
from virtex.serial import encode_bytes


# Get load test config from environment
num_data = int(os.getenv('NUM_QUERIES', 9000))
request_batch_size = int(os.getenv('REQUEST_BATCH_SIZE', 6))
client_rps = int(os.getenv('CLIENT_REQUESTS_PER_SECOND', 3500))
service_host = os.getenv('VIRTEX_SVC_NAME', 'http://127.0.0.1')
service_port = int(os.getenv('VIRTEX_SVC_PORT', 8081))
if service_host.startswith('http'):
    service_url = f'{service_host}:{service_port}'
else:
    service_url = f'http://{service_host}.virtex.svc.cluster.local:{service_port}'

# Load data
data = []
path = os.path.dirname(os.path.abspath(__file__))
for fn in glob(os.path.join(
        path, '../../data/tiny-imagenet-200/test/images/*.JPEG'))[:num_data]:
    data.append(open(fn, 'rb').read())
num_pad = num_data - len(data)
if num_pad > 0:
    for i in range(num_pad):
        data.append(data[np.random.randint(0, len(data))])
messages = []
for i in range(0, num_data, request_batch_size):
    message = HttpMessage(data=data[i:i + request_batch_size])
    message.encode(encode_bytes)
    messages.append(message)

# Run load test
client = HttpLoadTest()
result = client.run(service_url,
                    messages,
                    requests_per_second=client_rps)
pprint.pprint(result.metrics.dict(), indent=3)
