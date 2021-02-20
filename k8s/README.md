# k8s resource manifests

#### Run the following commands to spin up the benchmark test resources in your environment.

#### Create a dedicated namespace
    $ kubectl apply -f namespace.yaml

#### Install nvidia-device-plugin (only on gpu cluster)
    $ kubectl apply -f nvidia-device-plugin.yaml

#### Updated `configmaps.yaml` to configure load test, then
    $ kubectl apply -f configmaps.yaml

#### Install Prometheus pushgateway
    $ kubectl apply -f pushgateway.yaml

#### Launch server
    $ kubectl apply -f virtex-service.yaml

#### Run load test
    $ kubectl apply -f virtex-client.yaml

#### Get results
    $ kubectl logs -n virtex virtex-l<TAB>