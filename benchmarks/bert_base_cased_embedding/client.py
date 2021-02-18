import os
import pprint

from virtex import HttpMessage, HttpLoadTest


# Get load test config from environment
num_data = int(os.getenv('NUM_INFERENCES', 9000))
request_batch_size = int(os.getenv('REQUEST_BATCH_SIZE', 6))
client_rps = int(os.getenv('CLIENT_REQUESTS_PER_SECOND', 3500))
service_host = os.getenv('VIRTEX_SERVICE_HOST', 'http://127.0.0.1')
service_port = int(os.getenv('VIRTEX_SERVICE_PORT', 8081))

# Load data
fpath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../data/tweets.txt")
data = [line.strip().lower() for line in open(fpath, "r").readlines()]
messages = []
for i in range(0, num_data, request_batch_size):
    message = HttpMessage(data=data[i:i + request_batch_size])
    message.validate()
    messages.append(message)

# Run load test
client = HttpLoadTest()
url = f'{service_host}:{service_port}'
responses, metrics = client.run(url,
                                messages,
                                requests_per_second=client_rps)
pprint.pprint(metrics.dict(), indent=3)
