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

def get_config_path(filename):
    """Get the absolute path to a config file"""
    return Path(pkg_resources.resource_filename('comfystream', f'../configs/{filename}'))

def setup_model_files(config_path=None):
    """Download and setup required model files based on configuration"""
    if config_path is None:
        config_path = get_config_path('models.yaml')
    try:
        config = load_model_config(config_path)
    except FileNotFoundError:
        print(f"Error: Model config file not found at {config_path}")
        return
    # ... rest of the function ...

def install_custom_nodes(config_path=None):
    """Install custom nodes based on configuration"""
    if config_path is None:
        config_path = get_config_path('nodes.yaml')
    try:
        config = load_model_config(config_path)
    except FileNotFoundError:
        print(f"Error: Nodes config file not found at {config_path}")
        return
    # ... rest of the function ... 