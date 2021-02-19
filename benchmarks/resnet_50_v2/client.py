import os
import pprint
from glob import glob

import numpy as np

from virtex import HttpMessage, HttpLoadTest
from virtex.serial import encode_bytes


# Get load test config from environment
num_data = int(os.getenv('NUM_INFERENCES', 9000))
request_batch_size = int(os.getenv('REQUEST_BATCH_SIZE', 6))
client_rps = int(os.getenv('CLIENT_REQUESTS_PER_SECOND', 3500))
service_host = os.getenv('VIRTEX_SERVICE_HOST', '127.0.0.1')
service_port = int(os.getenv('VIRTEX_SERVICE_PORT', 8081))

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
url = f'http://{service_host}:{service_port}'
responses, metrics = client.run(url,
                                messages,
                                requests_per_second=client_rps)
pprint.pprint(metrics.dict())
