FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && bash ~/miniconda.sh -b -p /workspace/miniconda3 \
    && rm ~/miniconda.sh

# Add conda to path
ENV PATH="/workspace/miniconda3/bin:${PATH}"

# Create conda environments
RUN conda create -n comfyui python=3.11 -y \
    && conda create -n comfystream python=3.11 -y

# Set up shell initialization for conda
RUN echo ". /workspace/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc \
    && echo "conda activate comfystream" >> ~/.bashrc

# Create workspace directories
RUN mkdir -p /workspace/ComfyUI \
    && mkdir -p /workspace/comfyRealtime/ComfyUI \
    && mkdir -p /workspace/models

# Set working directory
WORKDIR /workspace

# The following directories will be mounted from host:
# - /workspace/miniconda3
# - /workspace/ComfyUI/models
# - /workspace/comfyRealtime

# (4) Clone the ComfyStream Setup Scripts and run initial_setup.sh
RUN git clone https://github.com/ryanontheinside/ComfyStream_Setup_Scripts \
    && chmod +x ./ComfyStream_Setup_Scripts/runpod/initial_setup.sh \
    # This script installs Miniconda, clones ComfyUI and ComfyStream,
    # creates conda environments, etc.
    && bash ./ComfyStream_Setup_Scripts/runpod/initial_setup.sh

# (5) Return to /app if that's where your code eventually lives
WORKDIR /app

COPY . /app
WORKDIR /app

