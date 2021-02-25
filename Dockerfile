FROM nvidia/cuda:11.1-base
MAINTAINER Chris Larson

RUN apt update -y && \
    apt install -y python3-dev python3-pip libcudnn8-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install \
        torch==1.7.1+cu110 \
        torchvision==0.8.2+cu110 \
        torchaudio===0.7.2 \
        -f https://download.pytorch.org/whl/torch_stable.html && \
    pip3 install \
        tensorflow \
        transformers \
        typing_extensions \
        virtex

COPY run.sh /root/virtex-benchmarks/
COPY data/ /root/virtex-benchmarks/data/
COPY benchmarks /root/virtex-benchmarks/benchmarks

# Entrypoint
EXPOSE 8081/tcp
ENTRYPOINT ["/bin/bash", "-l", "/root/virtex-benchmarks/run.sh"]