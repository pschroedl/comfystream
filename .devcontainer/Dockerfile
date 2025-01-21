FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace \
    && cd /workspace \
    && git clone https://github.com/ryanontheinside/ComfyStream_Setup_Scripts \
    && cp ./ComfyStream_Setup_Scripts/runpod/new_server_setup.sh new_server_setup.sh \
    && bash ./ComfyStream_Setup_Scripts/runpod/initial_setup.sh

RUN cd /workspace \
    && sed -i '1i\export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID_HERE"\nexport TWILIO_AUTH_TOKEN="YOUR_AUTH_TOKEN_HERE"\n' new_server_setup.sh \
    && bash ./new_server_setup.sh


RUN cd /workspace \
    && eval "$(/workspace/miniconda3/bin/conda shell.bash hook)" \
    && conda activate comfyui

    # Install ComfyUI nodes from nodes.yaml
    RUN cd /workspace/ComfyUI/custom_nodes && \
        # Core TensorRT nodes
        git clone -b quantization_with_controlnet_fixes https://github.com/yondonfu/ComfyUI_TensorRT && \
        && cd ComfyUI_TensorRT \
        && pip install -r requirements.txt \
        && cd .. \
        && git clone https://github.com/yuvraj108c/ComfyUI-Depth-Anything-Tensorrt \
        && cd ComfyUI-Depth-Anything-Tensorrt \
        && pip install -r requirements.txt \
        && cd .. \
        # Ryan's nodes
        git clone https://github.com/pschroedl/ComfyUI_RyanOnTheInside.git \
        && cd ComfyUI_RyanOnTheInside \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/ltdrdata/ComfyUI-Manager.git \
        && cd ComfyUI-Manager \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/ryanontheinside/ComfyUI-Misc-Effects.git \
        && cd ComfyUI-Misc-Effects \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/ryanontheinside/ComfyUI_RealTimeNodes.git \
        && cd ComfyUI_RealTimeNodes \
        && pip install -r requirements.txt \
        && cd .. \
        # Vision and AI nodes
        git clone https://github.com/ad-astra-video/ComfyUI-Florence2-Vision.git \
        && cd ComfyUI-Florence2-Vision \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/pschroedl/ComfyUI-SAM2-Realtime.git \
        && cd ComfyUI-SAM2-Realtime \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/pschroedl/ComfyUI-StreamDiffusion.git \
        && cd ComfyUI-StreamDiffusion \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/kijai/ComfyUI-LivePortraitKJ.git \
        && cd ComfyUI-LivePortraitKJ \
        && pip install -r requirements.txt \
        && cd .. \
        # Utility nodes
        git clone https://github.com/tsogzark/ComfyUI-load-image-from-url.git \
        && cd ComfyUI-load-image-from-url \
        && pip install -r requirements.txt \
        && cd .. \
        git clone https://github.com/yondonfu/ComfyUI-Torch-Compile \
        && cd ComfyUI-Torch-Compile \
        && pip install -r requirements.txt \
        && cd ../../../comfyRealtime \

    # Install additional dependencies
    RUN pip install opencv-python

    RUN conda deactivate \
    && conda activate comfystream \ 
    && python install.py --workspace ../ComfyUI
