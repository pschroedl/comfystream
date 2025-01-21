#!/usr/bin/env bash
set -e

# Check if ComfyUI is already installed
if [ ! -d "/workspace/ComfyUI" ]; then
  echo "No existing ComfyUI installation found. Running initial setup..."

  # Example commands:
  # We assume your Dockerfile has installed git, etc.
  cd /workspace
  git clone https://github.com/ryanontheinside/ComfyStream_Setup_Scripts
  cp ./ComfyStream_Setup_Scripts/runpod/new_server_setup.sh new_server_setup.sh
  bash ./ComfyStream_Setup_Scripts/runpod/initial_setup.sh

  # Optionally store Twilio creds if you didn't pass them in via environment
  sed -i "1i\\
  export TWILIO_ACCOUNT_SID=\"${TWILIO_ACCOUNT_SID}\"\n\
  export TWILIO_AUTH_TOKEN=\"${TWILIO_AUTH_TOKEN}\"\n" new_server_setup.sh

  # This script starts both ComfyUI and ComfyStream envs
  bash ./new_server_setup.sh

  #############################################
  # >> INSERT CUSTOM NODE INSTALLATION HERE <<
  #############################################

  echo "Installing custom nodes in comfyui environment..."
  # Activate comfyui environment
  source /workspace/miniconda3/etc/profile.d/conda.sh
  conda activate comfyui

  cd /workspace/ComfyUI/custom_nodes

  # Core TensorRT nodes
  git clone -b quantization_with_controlnet_fixes https://github.com/yondonfu/ComfyUI_TensorRT
  cd ComfyUI_TensorRT
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/yuvraj108c/ComfyUI-Depth-Anything-Tensorrt
  cd ComfyUI-Depth-Anything-Tensorrt
  pip install -r requirements.txt
  cd ..

  # Ryan's nodes
  git clone https://github.com/pschroedl/ComfyUI_RyanOnTheInside.git
  cd ComfyUI_RyanOnTheInside
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/ltdrdata/ComfyUI-Manager.git
  cd ComfyUI-Manager
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/ryanontheinside/ComfyUI-Misc-Effects.git
  cd ComfyUI-Misc-Effects
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/ryanontheinside/ComfyUI_RealTimeNodes.git
  cd ComfyUI_RealTimeNodes
  pip install -r requirements.txt
  cd ..

  # Vision and AI nodes
  git clone https://github.com/ad-astra-video/ComfyUI-Florence2-Vision.git
  cd ComfyUI-Florence2-Vision
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/pschroedl/ComfyUI-SAM2-Realtime.git
  cd ComfyUI-SAM2-Realtime
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/pschroedl/ComfyUI-StreamDiffusion.git
  cd ComfyUI-StreamDiffusion
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/kijai/ComfyUI-LivePortraitKJ.git
  cd ComfyUI-LivePortraitKJ
  pip install -r requirements.txt
  cd ..

  # Utility nodes
  git clone https://github.com/tsogzark/ComfyUI-load-image-from-url.git
  cd ComfyUI-load-image-from-url
  pip install -r requirements.txt
  cd ..

  git clone https://github.com/yondonfu/ComfyUI-Torch-Compile
  cd ComfyUI-Torch-Compile
  pip install -r requirements.txt
  cd ..

  # Example: installing opencv for both environments
  pip install opencv-python

  # Deactivate, then optionally do similar logic for comfystream environment
  conda deactivate
  conda activate comfystream
  # (If you want to replicate some of the same nodes in comfystream env, you'd do it here)
  python install.py --workspace ../ComfyUI

  conda deactivate

else
  echo "Found existing ComfyUI installation. Starting new_server_setup..."
  cd /workspace

  # Optionally re-inject Twilio credentials if needed
  sed -i "1i\\
  export TWILIO_ACCOUNT_SID=\"${TWILIO_ACCOUNT_SID}\"\n\
  export TWILIO_AUTH_TOKEN=\"${TWILIO_AUTH_TOKEN}\"\n" new_server_setup.sh

  bash ./new_server_setup.sh
fi

echo "Setup complete. Tailing to keep container running..."
tail -f /dev/null 