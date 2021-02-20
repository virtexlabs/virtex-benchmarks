import os

from virtex import http_server, RequestHandler


max_batch_size = int(os.getenv('MAX_BATCH_SIZE', 512))
max_time_on_queue = float(os.getenv('MAX_TIME_ON_QUEUE', 0.01))
metrics_interval = float(os.getenv('METRICS_INTERVAL', 0.05))
metrics_host = os.getenv('PUSHGATEWAY_SVC_NAME', 'http://127.0.0.1')
metrics_port = int(os.getenv('PUSHGATEWAY_SVC_PORT', 9091))


class EchoServer(RequestHandler):

    def process_request(self, data):
        return data

    def run_inference(self, model_input):
        return model_input

    def process_response(self, model_output_item):
        return model_output_item


app = http_server(
    name='echo_service',
    handler=EchoServer(),
    max_batch_size=max_batch_size,
    max_time_on_queue=max_time_on_queue,
    metrics_host=metrics_host,
    metrics_port=metrics_port,
    metrics_mode='push',
    metrics_interval=metrics_interval
)
