import unittest
from pathlib import Path
import yaml
import os

class TestDepthAnythingInstallation(unittest.TestCase):
    def setUp(self):
        self.comfyui_path = Path("/comfyui")
        self.models_path = self.comfyui_path / "models"
        self.custom_nodes_path = self.comfyui_path / "custom_nodes"
        
        # Load configs
        with open("configs/nodes.yaml", 'r') as f:
            self.nodes_config = yaml.safe_load(f)
        with open("configs/models.yaml", 'r') as f:
            self.models_config = yaml.safe_load(f)
            
        # Required components for depth-anything workflow
        self.required_nodes = [
            "comfyui-tensorrt",
            "comfyui-depthanything-tensorrt",
            "comfyui-depth-anything",
        ]
        
        self.required_models = [
            "depth-anything-onnx",
        ]

    def test_base_directories_exist(self):
        """Test if base directories are properly created"""
        self.assertTrue(self.comfyui_path.exists(), "ComfyUI base directory not found")
        self.assertTrue(self.models_path.exists(), "Models directory not found")
        self.assertTrue(self.custom_nodes_path.exists(), "Custom nodes directory not found")

    def test_required_nodes_installed(self):
        """Test if all required custom nodes are installed"""
        for node_id in self.required_nodes:
            node_info = self.nodes_config['nodes'][node_id]
            dir_name = node_info['url'].split("/")[-1].replace(".git", "")
            node_path = self.custom_nodes_path / dir_name
            
            self.assertTrue(
                node_path.exists(), 
                f"Required node {node_info['name']} not found at {node_path}"
            )
            
            # Check if requirements.txt was processed if it exists
            requirements_file = node_path / "requirements.txt"
            if requirements_file.exists():
                self.assertTrue(
                    self._check_requirements_installed(requirements_file),
                    f"Requirements not fully installed for {node_info['name']}"
                )

    def test_required_models_present(self):
        """Test if all required models are downloaded"""
        for model_id in self.required_models:
            model_info = self.models_config['models'][model_id]
            
            # Determine the full path based on whether it's in custom_nodes or models
            if model_info['path'].startswith('custom_nodes/'):
                full_path = self.comfyui_path / model_info['path']
            else:
                full_path = self.models_path / model_info['path']
            
            self.assertTrue(
                full_path.exists(), 
                f"Required model {model_info['name']} not found at {full_path}"
            )
            
            # Check extra files if any
            if 'extra_files' in model_info:
                for extra in model_info['extra_files']:
                    extra_path = self.models_path / extra['path']
                    self.assertTrue(
                        extra_path.exists(),
                        f"Extra file {extra['path']} for {model_info['name']} not found"
                    )

    def test_depth_anything_workflow_loadable(self):
        """Test if the depth-anything workflow file exists and is valid"""
        workflow_path = Path("workflows/depth-anything-v2-trt-example-workflow.json")
        self.assertTrue(workflow_path.exists(), "Depth Anything workflow file not found")
        
        # Check if workflow file is valid JSON
        import json
        try:
            with open(workflow_path, 'r') as f:
                workflow = json.load(f)
            # Check for essential nodes in workflow
            node_types = {node['class_type'] for node in workflow.values() if isinstance(node, dict)}
            required_node_types = {'LoadImage', 'DepthAnythingTensorrt', 'PreviewImage'}
            self.assertTrue(
                required_node_types.issubset(node_types),
                f"Workflow missing required nodes. Expected {required_node_types}, found {node_types}"
            )
        except json.JSONDecodeError:
            self.fail("Workflow file is not valid JSON")

    def _check_requirements_installed(self, requirements_file):
        """Helper method to check if requirements from a file are installed"""
        import pkg_resources
        import re
        
        with open(requirements_file, 'r') as f:
            requirements = f.read().splitlines()
        
        try:
            for req in requirements:
                # Skip empty lines and comments
                if not req or req.startswith('#'):
                    continue
                # Remove any version specifiers
                package = re.split(r'[=<>]', req)[0].strip()
                pkg_resources.require(package)
            return True
        except pkg_resources.DistributionNotFound:
            return False

if __name__ == '__main__':
    unittest.main() 