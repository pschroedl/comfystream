# ComfyStream Configuration Guide

This guide explains how to customize ComfyStream's installation and components using configuration files.

## Configuration Files Overview

- `pyproject.toml`: Package dependencies and build settings
- `configs/models.yaml`: Model weights and checkpoints configuration
- `configs/nodes.yaml`: Custom ComfyUI nodes configuration

## Directory Structure

```
comfystream/
├── configs/
│   ├── models.yaml    # Model definitions
│   └── nodes.yaml     # Custom node definitions
├── pyproject.toml     # Package configuration
└── scripts/
    └── setup_nodes.py # Installation script
```

## Configuration Details

### 1. Custom Nodes (nodes.yaml)

Configure which ComfyUI nodes to install:

```yaml
nodes:
  # Core TensorRT nodes
  comfyui-tensorrt:
    name: "ComfyUI TensorRT"
    url: "https://github.com/yondonfu/ComfyUI_TensorRT"
    type: "tensorrt"

  # Add custom nodes with optional dependencies
  comfyui-realtimenode:
    name: "ComfyUI RealTimeNodes"
    url: "https://github.com/ryanontheinside/ComfyUI_RealTimeNodes.git"
    type: "realtime"
    dependencies:
      - "opencv-python"
```

Available fields:
- `name`: Human-readable name
- `url`: Git repository URL
- `type`: Node category/type
- `dependencies`: Additional Python packages needed (optional)
- `branch`: Specific git branch or commit (optional)

### 2. Models (models.yaml)

Define model weights to download:

```yaml
models:
  # Base models
  dreamshaper-v8:
    name: "Dreamshaper v8"
    url: "https://civitai.com/api/download/models/128713"
    path: "checkpoints/SD1.5/dreamshaper-8.safetensors"
    type: "checkpoint"

  # Models with additional files
  dreamshaper-dmd:
    name: "Dreamshaper DMD"
    url: "https://huggingface.co/aaronb/dreamshaper-8-dmd-1kstep/resolve/main/diffusion_pytorch_model.safetensors"
    path: "unet/dreamshaper-8-dmd-1kstep.safetensors"
    type: "unet"
    extra_files:
      - url: "https://huggingface.co/aaronb/dreamshaper-8-dmd-1kstep/raw/main/config.json"
        path: "unet/dreamshaper-8-dmd-1kstep.json"
```

Available fields:
- `name`: Human-readable name
- `url`: Download URL
- `path`: Installation path (relative to workspace)
- `type`: Model type
- `extra_files`: Additional files to download (optional)

### 3. Package Dependencies (pyproject.toml)

Add required Python packages:

```toml
[project.dependencies]
# Core dependencies
torch = "==2.5.1"
tensorrt = "==10.6.0"
opencv-python = "*"

[project.optional-dependencies]
custom-nodes = [
    # Pip-installable custom nodes
    "comfy-tensorrt @ git+https://github.com/yondonfu/ComfyUI_TensorRT.git",
]
```

## Usage

### Installation

```bash
# Install the package with configs
pip install -e .

# Default installation (~/comfyui)
setup-comfyui-nodes

# Custom workspace
setup-comfyui-nodes --workspace /path/to/workspace

# Using environment variable
export COMFY_UI_WORKSPACE=/path/to/workspace
setup-comfyui-nodes
```

### Adding New Components

1. **New Custom Node**:
   ```yaml
   # In configs/nodes.yaml
   nodes:
     my-custom-node:
       name: "My Custom Node"
       url: "https://github.com/user/my-custom-node"
       type: "custom"
       dependencies:
         - "required-package"
   ```

2. **New Model**:
   ```yaml
   # In configs/models.yaml
   models:
     my-model:
       name: "My Model"
       url: "https://example.com/model.safetensors"
       path: "checkpoints/my-model.safetensors"
       type: "checkpoint"
   ```

3. **New Dependency**:
   ```toml
   # In pyproject.toml
   [project.dependencies]
   new-package = ">=1.0.0"
   ```

### Testing

Verify your configuration:
```bash
python -m unittest tests/test_installation.py
```

## Workspace Structure

```
workspace/
├── custom_nodes/          # Installed custom nodes
└── models/
    ├── checkpoints/      # Model checkpoints
    ├── controlnet/       # ControlNet models
    ├── unet/            # UNet models
    ├── vae/             # VAE models
    └── tensorrt/        # TensorRT engines
```

## Notes

- All paths in `models.yaml` are relative to the workspace directory
- Custom nodes are installed from Git repositories
- Dependencies listed in `nodes.yaml` are installed automatically
- The script creates all necessary directories
- Models are downloaded only if they don't exist 