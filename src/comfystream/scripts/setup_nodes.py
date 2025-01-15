#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
import shutil
import requests
from tqdm import tqdm
import yaml
import pkg_resources
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Setup ComfyUI nodes and models')
    parser.add_argument('--workspace', 
                       default=os.environ.get('COMFY_UI_WORKSPACE', os.path.expanduser('~/comfyui')),
                       help='ComfyUI workspace directory (default: ~/comfyui or $COMFY_UI_WORKSPACE)')
    return parser.parse_args()

def get_config_path(filename):
    """Get the absolute path to a config file"""
    # First try the local configs directory
    local_path = Path("configs") / filename
    if local_path.exists():
        return local_path
        
    # Then try the installed configs directory
    installed_path = Path(sys.prefix) / "configs" / filename
    if installed_path.exists():
        return installed_path
        
    raise FileNotFoundError(f"Config file {filename} not found in either {local_path} or {installed_path}")

def setup_environment(workspace_dir):
    os.environ["COMFY_UI_WORKSPACE"] = str(workspace_dir)
    os.environ["PYTHONPATH"] = str(workspace_dir)
    os.environ["CUSTOM_NODES_PATH"] = str(workspace_dir / "custom_nodes")

def download_file(url, destination, description=None):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    desc = description or os.path.basename(destination)
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=desc)
    
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    with open(destination, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)
    progress_bar.close()

def load_model_config(config_path):
    """Load model configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_model_files(workspace_dir, config_path=None):
    """Download and setup required model files based on configuration"""
    if config_path is None:
        config_path = get_config_path('models.yaml')
    try:
        config = load_model_config(config_path)
    except FileNotFoundError:
        print(f"Error: Model config file not found at {config_path}")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing model config file: {e}")
        return

    models_path = workspace_dir / "models"
    base_path = workspace_dir

    for model_id, model_info in config['models'].items():
        # Determine the full path based on whether it's in custom_nodes or models
        if model_info['path'].startswith('custom_nodes/'):
            full_path = base_path / model_info['path']
        else:
            full_path = models_path / model_info['path']

        if not full_path.exists():
            print(f"Downloading {model_info['name']}...")
            download_file(
                model_info['url'],
                full_path,
                f"Downloading {model_info['name']}"
            )
            print(f"Downloaded {model_info['name']} to {full_path}")

            # Handle any extra files (like configs)
            if 'extra_files' in model_info:
                for extra in model_info['extra_files']:
                    extra_path = models_path / extra['path']
                    if not extra_path.exists():
                        download_file(
                            extra['url'],
                            extra_path,
                            f"Downloading {os.path.basename(extra['path'])}"
                        )

def setup_directories(workspace_dir):
    """Create required directories in the workspace"""
    # Create base directories
    workspace_dir.mkdir(parents=True, exist_ok=True)
    custom_nodes_dir = workspace_dir / "custom_nodes"
    models_dir = workspace_dir / "models"
    
    custom_nodes_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Create model subdirectories
    model_dirs = [
        "checkpoints/SD1.5",
        "controlnet",
        "vae",
        "tensorrt",
        "unet",
    ]
    for dir_name in model_dirs:
        (models_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Create symlink for models if /models/ComfyUI--models exists
    models_source = Path("/models/ComfyUI--models")
    if models_source.exists():
        if not models_dir.exists():
            models_dir.symlink_to(models_source)

def install_custom_nodes(workspace_dir, config_path=None):
    """Install custom nodes based on configuration"""
    if config_path is None:
        config_path = get_config_path('nodes.yaml')
    try:
        config = load_model_config(config_path)
    except FileNotFoundError:
        print(f"Error: Nodes config file not found at {config_path}")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing nodes config file: {e}")
        return

    custom_nodes_path = workspace_dir / "custom_nodes"
    custom_nodes_path.mkdir(parents=True, exist_ok=True)
    os.chdir(custom_nodes_path)
    
    for node_id, node_info in config['nodes'].items():
        dir_name = node_info['url'].split("/")[-1].replace(".git", "")
        node_path = custom_nodes_path / dir_name
        
        if not node_path.exists():
            print(f"Installing {node_info['name']}...")
            
            # Clone the repository
            cmd = ["git", "clone", node_info['url']]
            if 'branch' in node_info:
                cmd.extend(["-b", node_info['branch']])
            subprocess.run(cmd, check=True)
            
            # Checkout specific commit if branch is a commit hash
            if 'branch' in node_info and len(node_info['branch']) == 40:  # SHA-1 hash length
                subprocess.run(["git", "-C", dir_name, "checkout", node_info['branch']], check=True)
            
            # Install requirements if present
            requirements_file = node_path / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
            
            # Install additional dependencies if specified
            if 'dependencies' in node_info:
                for dep in node_info['dependencies']:
                    subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            
            print(f"Installed {node_info['name']}")
        else:
            print(f"{node_info['name']} already installed")

def main():
    args = parse_args()
    workspace_dir = Path(args.workspace)
    
    setup_environment(workspace_dir)
    setup_directories(workspace_dir)
    install_custom_nodes(workspace_dir)
    setup_model_files(workspace_dir)

if __name__ == "__main__":
    main() 