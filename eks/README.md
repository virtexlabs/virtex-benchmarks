# k8s cluster manifests

#### The below commands assume that you have properly configured versions of `aws` and `eksctl` on your local machine that are connected to an AWS account. Note that the cluster will take between 10-30 minutes to spin up.

#### CPU cluster (~$6/hr)
    $ eksctl create cluster -f cluster-cpu.yaml

#### GPU cluster (~$50/hr)
    $ eksctl create cluster -f cluster-gpu.yaml

#### To delete your cluster:
    $ eksctl delete cluster --region=<region-name> --name=virtex-perf