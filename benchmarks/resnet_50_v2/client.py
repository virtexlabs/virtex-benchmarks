import os
import sys
import pprint
from glob import glob

import tqdm

from virtex import HttpMessage, HttpLoadTest
from virtex.serial import encode_bytes


def run():
    """
    Running this requires the Resnet50V2 model and Imagenet data. Keras will
    automatically download the pretrained model when the model get's invoked,
    you can download the Imagenet data by running data/get_tiny_imagenet.sh.
    """
    images = []
    bar = tqdm.tqdm(total=N)
    bar.set_description("Loading imagenet test set")
    for fn in glob(os.path.join(
            path, '../../data/tiny-imagenet-200/test/images/*.JPEG'))[:N]:
        images.append(open(fn, 'rb').read())
        bar.update(1)
    bar.close()
    messages = []
    for i in range(0, N, M):
        message = HttpMessage(data=images[i: i + M])
        message.encode(encode_bytes)
        messages.append(message)
    url = 'http://127.0.0.1:8081'
    client = HttpLoadTest()
    responses, metrics = client.run(url, messages, requests_per_second=R)
    pprint.pprint(metrics.dict())


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    N = int(sys.argv[1])    # number of data elements
    M = int(sys.argv[2])    # request batch size
    R = int(sys.argv[3])    # client load (in requests per second)
    run()
