import sys
import pprint

from virtex import HttpLoadTest, HttpMessage


def run_virtex_bert_embedding_client():

    payload = "X" * content_length

    # Get text data
    messages = []
    for i in range(0, N, M):
        message = HttpMessage(data=[payload for _ in range(M)])
        message.validate()
        messages.append(message)

    # Instantiate client
    url = 'http://127.0.0.1:8081'
    client = HttpLoadTest()

    # Run load test
    responses, metrics = client.run(url, messages, requests_per_second=R)
    pprint.pprint(metrics.dict())


if __name__ == '__main__':
    N = int(sys.argv[1])                # number of data elements
    M = int(sys.argv[2])                # request batch size
    R = int(sys.argv[3])                # client load (in requests per second)
    n = N // M                          # number of requests
    content_length = int(sys.argv[4])   # content length
    run_virtex_bert_embedding_client()
