#!/bin/bash

# Create a symlink to the ComfyUI workspace
if [ ! -d "/workspace/ComfyUI" ]; then
    ln -s /ComfyUI /workspace/ComfyUI
fi

# Create a symlink to the extra_model_paths.yaml file
if [ ! -d "/ComfyUI/extra_model_paths.yaml" ]; then
    ln -s /workspace/.devcontainer/extra_model_paths.yaml /ComfyUI/extra_model_paths.yaml
fi

# Create a symlink to the tensor_utils directory to make it easier to develop comfystream nodes
if [ ! -d "/ComfyUI/custom_nodes/tensor_utils" ]; then
    ln -s /workspace/nodes/tensor_utils /ComfyUI/custom_nodes/tensor_utils
fi

# Initialize conda if needed
if ! command -v conda &> /dev/null; then
    /miniconda3/bin/conda init bash
fi

source ~/.bashrc
