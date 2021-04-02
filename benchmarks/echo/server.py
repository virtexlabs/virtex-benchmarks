import os

from virtex import http_server, RequestHandler


max_batch_size = int(os.getenv('MAX_BATCH_SIZE', 2500))
max_time_on_queue = float(os.getenv('MAX_TIME_ON_QUEUE', 0.01))
prom_interval = float(os.getenv('PROMETHEUS_INTERVAL', 0.05))
prom_host = os.getenv('PROMETHEUS_HOST', 'http://127.0.0.1')
prom_port = int(os.getenv('PROMETHEUS_PORT', 9090))
prom_mode = os.getenv('PROMETHEUS_MODE', 'off')


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
    prom_host=prom_host,
    prom_port=prom_port,
    prom_mode=prom_mode,
    prom_push_interval=prom_interval
)
