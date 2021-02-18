import os

from PIL import Image
import torch
from torchvision.models import resnet50
from torchvision import transforms

from virtex import RequestHandler, \
    http_server, HttpMessage
from virtex.serial import encode_bytes, encode_pickle, \
    decode_pil_from_bytes


max_batch_size = int(os.getenv('MAX_BATCH_SIZE', 56))
max_time_on_queue = float(os.getenv('MAX_TIME_ON_QUEUE', 0.01))
metrics_interval = float(os.getenv('METRICS_INTERVAL', 0.05))
metrics_host = os.getenv('PUSHGATEWAY_SERVICE_HOST', 'http://127.0.0.1')
metrics_port = int(os.getenv('PUSHGATEWAY_SERVICE_PORT', 9091))


# Build ResNet50 request handler
class Resnet50Computation(RequestHandler):

    enable_cuda = True if torch.cuda.is_available() else False
    model = resnet50()
    model.eval()
    if enable_cuda:
        model.cuda(torch.device('cuda'))
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])

    def process_request(self, data):
        imgs = []
        for i, item in enumerate(data):
            img = decode_pil_from_bytes(item)
            img = img.convert('RGB')
            img = img.resize((224, 224), Image.NEAREST)
            imgs.append(self.transform(img))
        data = torch.stack(imgs, dim=0)
        return data

    def run_inference(self, model_input):
        if self.enable_cuda:
            model_input = model_input.to('cuda')
        return self.model(model_input)

    def process_response(self, model_output_item):
        return encode_pickle(
            model_output_item.cpu().detach().numpy())


# Create http test messages
path = os.path.dirname(os.path.abspath(__file__))
image = open(os.path.join(
    path, "../../data/tiny-imagenet-200/test/images/test_0.JPEG"
), 'rb').read()

# Create messages with encoded payloads
message1 = HttpMessage(data=[image])
message1.encode(encode_bytes)
message2 = HttpMessage(data=[image for _ in range(max_batch_size)])
message2.encode(encode_bytes)

# Validate that handler can process messages
resnet_request_handler = Resnet50Computation()
assert resnet_request_handler.validate(message1)
assert resnet_request_handler.validate(message2)

# Create http server
app = http_server(
    name='resnet_50_v2_service',
    handler=Resnet50Computation(),
    max_batch_size=max_batch_size,
    max_time_on_queue=max_time_on_queue,
    metrics_host=metrics_host,
    metrics_port=metrics_port,
    metrics_mode='push',
    metrics_interval=metrics_interval
)
