import os
import pprint

from virtex import HttpLoadTest, HttpMessage


# Get load test config from environment
num_data = int(os.getenv('NUM_QUERIES', 9000))
request_batch_size = int(os.getenv('REQUEST_BATCH_SIZE', 6))
client_rps = int(os.getenv('CLIENT_REQUESTS_PER_SECOND', 3500))
content_length = int(os.getenv('CONTENT_LENGTH', 100))
service_host = os.getenv('VIRTEX_SVC_NAME', 'http://127.0.0.1')
service_port = int(os.getenv('VIRTEX_SVC_PORT', 8081))
if service_host.startswith('http'):
    service_url = f'{service_host}:{service_port}'
else:
    service_url = f'http://{service_host}.virtex.svc.cluster.local:{service_port}'

# Load data
payload = "X" * content_length
messages = []
for i in range(0, num_data, request_batch_size):
    message = HttpMessage(data=[payload for _ in range(request_batch_size)])
    message.validate()
    messages.append(message)

# Run load test
client = HttpLoadTest()
responses, metrics = client.run(service_url,
                                messages,
                                requests_per_second=client_rps)
pprint.pprint(metrics.dict())
