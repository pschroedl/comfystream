#!/bin/bash

# Define arrays of workflows and models
WORKFLOWS=(
    "workflows/ui/1 - Build ONNX.json"
    "workflows/ui/2 - Build TensorRT.json"
    "workflows/ui/3 - Convert TensorRT.json"
)

MODELS=(
    "v1-5-pruned.safetensors"
    "dreamshaper_8.safetensors"
    "deliberate_v2.safetensors"
)

# Function to process a workflow with a specific model
process_workflow() {
    local workflow_file="$1"
    local model_name="$2"
    
    echo "Processing workflow: $workflow_file with model: $model_name"
    
    # Load and modify the workflow JSON
    MODIFIED_JSON=$(cat "$workflow_file" | sed "s/[^\"]*\.safetensors/$model_name/g")
    
    # Show the modification (optional, for debugging)
    echo "Modified workflow:"
    echo "$MODIFIED_JSON" | jq '.'
    
    # Format for the API
    WORKFLOW=$(echo "$MODIFIED_JSON" | jq -c '{prompt: .}')
    
    # Confirm before sending (optional, for testing)
    read -p "Send this request? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping..."
        return
    fi
    
    # Send the request
    RESPONSE=$(curl -s -X POST \
        http://127.0.0.1:8188/prompt \
        -H 'Content-Type: application/json' \
        -d "$WORKFLOW")
    
    # Check response
    if [ $? -eq 0 ]; then
        echo "Successfully processed with $model_name"
        echo "Response: $RESPONSE"
    else
        echo "Error: Failed to send request"
    fi
    
    sleep 2
}

# Main loop
for workflow in "${WORKFLOWS[@]}"; do
    for model in "${MODELS[@]}"; do
        process_workflow "$workflow" "$model"
    done
done
