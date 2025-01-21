FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano \
    socat \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace

# 2. Install Miniconda (optional, if you want it ready at build-time)
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /workspace/miniconda3 \
    && rm /tmp/miniconda.sh
ENV PATH="/workspace/miniconda3/bin:${PATH}"

# 3. Copy in init_or_start.sh (optional; if you're mounting /app anyway, you can skip)
COPY app/init_or_start.sh /app/init_or_start.sh
RUN chmod +x /app/init_or_start.sh

# 4. Set the default working directory
WORKDIR /workspace

RUN cd /workspace \
    && eval "$(/workspace/miniconda3/bin/conda shell.bash hook)"

