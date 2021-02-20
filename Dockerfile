FROM fedora:33
MAINTAINER Chris Larson

# Conda
RUN dnf install -y \
    wget \
    bzip2 \
    libXcomposite \
    libXcursor \
    libXi \
    libXtst \
    libXrandr \
    alsa-lib \
    mesa-libEGL \
    libXdamage \
    mesa-libGL \
    libXScrnSaver
RUN wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    chmod +x ~/anaconda.sh && \
    bash ~/anaconda.sh -b -p $HOME/anaconda && \
    rm -f ~/anaconda.sh && \
    source $HOME/anaconda/bin/activate base && \
    $HOME/anaconda/bin/conda create -n 'virtex' python=3.8.5 && \
    source $HOME/anaconda/bin/activate virtex && \
    $HOME/anaconda/bin/conda install -c anaconda cudatoolkit==11.0.221 && \
    echo 'export PATH="$HOME/anaconda/bin${PATH:+:${PATH}}"' >> ~/.bashrc && \
    echo 'export PATH=$HOME/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/bin${PATH:+:${PATH}}' >> ~/.bashrc && \
    echo 'export LD_LIBRARY_PATH=$HOME/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/lib:$HOME/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc && \
    echo 'source activate virtex' >> ~/.bashrc && \
    mkdir -p /root/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/lib64 && \
    mkdir -p /root/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/include && \
    mkdir -p /root/virtex-benchmarks && \
    $HOME/anaconda/bin/conda clean --all

# CUDA
COPY docker/cuda/ /root/anaconda/pkgs/cudatoolkit-11.0.221-h6bb024c_0/

# Virtex
COPY docker/whl /root/virtex-benchmarks/docker/whl
COPY requirements.txt /root/virtex-benchmarks/
RUN cd /root/virtex-benchmarks && \
    source ~/.bashrc && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt && \
    python -m pip install virtex && \
    conda clean --all
COPY run.sh /root/virtex-benchmarks/
COPY data/ /root/virtex-benchmarks/data/
COPY benchmarks /root/virtex-benchmarks/benchmarks

# Config
ENV TASK='' \
    LOG_LEVEL='' \
    VIRTEX_SVC_NAME='' \
    VIRTEX_SVC_PORT='' \
    VIRTEX_TARGET_PORT='' \
    PUSHGATEWAY_SVC_NAME='' \
    PUSHGATEWAY_SVC_PORT='' \
    MAX_CONCURRENT_CONNECTIONS='' \
    NUM_VIRTEX_WORKERS='' \
    MAX_BATCH_SIZE='' \
    MAX_TIME_ON_QUEUE='' \
    METRICS_INTERVAL='' \
    MAX_SEQUENCE_LENGTH='' \
    NUM_INFERENCES='' \
    CLIENT_REQUESTS_PER_SECOND='' \
    REQUEST_BATCH_SIZE='' \
    CONTENT_LENGTH=''

# Entrypoint
EXPOSE 8081/tcp
ENTRYPOINT ["/bin/bash", "-l", "/root/virtex-benchmarks/run.sh"]