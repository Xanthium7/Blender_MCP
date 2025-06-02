# BlenderMCP - Blender Model Context Protocol Server

BlenderMCP is a Model Context Protocol (MCP) server that enables AI assistants to interact with Blender through a standardized interface. It provides tools for scene manipulation, asset creation, and integration with external services like PolyHaven and Hyper3D Rodin.

## Features

- **Scene Information**: Get detailed information about Blender scenes and objects
- **Code Execution**: Execute Python code directly in Blender
- **PolyHaven Integration**: Download and apply HDRIs, textures, and 3D models
- **Hyper3D Rodin Integration**: Generate 3D assets from text prompts or images
- **Real-time Communication**: WebSocket-based communication with Blender

## Prerequisites

- **Blender** (version 3.0 or higher)
- **Python** (version 3.8 or higher)
- **BlenderMCP Addon** (must be installed and running in Blender)

## Installation

### 1. Install Python Dependencies

```bash
# Install required packages
pip install mcp fastmcp nest-asyncio
```

### 2. Install BlenderMCP Addon in Blender

1. Download the BlenderMCP addon
2. Open Blender
3. Go to Edit → Preferences → Add-ons
4. Click "Install..." and select the addon file
5. Enable the "BlenderMCP" addon
6. Configure the addon settings in the sidebar

### 3. Configure Integrations (Optional)

#### PolyHaven Integration
- Enable PolyHaven in the BlenderMCP addon sidebar
- No API key required (uses free API)

#### Hyper3D Rodin Integration
- Enable Hyper3D in the BlenderMCP addon sidebar
- Choose between:
  - **MAIN_SITE mode**: Requires Hyper3D API key from hyper3d.ai
  - **FAL_AI mode**: Requires FAL API key from fal.ai
  - **Free Trial**: Limited daily generations

## Usage

### Starting the Server

1. **Start Blender** and ensure the BlenderMCP addon is enabled
2. **Run the MCP server**:
   ```bash
   python server.py
   ```
   The server will start on `http://localhost:8000`

### Testing with Client

Run the test client to verify everything works:

```bash
python client_sse.py
```

### Available Tools

#### Core Tools
- `get_scene_info()` - Get detailed information about the current scene
- `get_object_info(object_name)` - Get information about a specific object
- `execute_blender_code(code)` - Execute Python code in Blender

#### PolyHaven Tools
- `get_polyhaven_status()` - Check if PolyHaven integration is enabled
- `get_polyhaven_categories(asset_type)` - List available categories
- `search_polyhaven_assets(asset_type, categories)` - Search for assets
- `download_polyhaven_asset(asset_id, asset_type, resolution, file_format)` - Download and import assets
- `set_texture(object_name, texture_id)` - Apply textures to objects

#### Hyper3D Rodin Tools
- `get_hyper3d_status()` - Check if Hyper3D integration is enabled
- `generate_hyper3d_model_via_text(text_prompt, bbox_condition)` - Generate 3D models from text
- `generate_hyper3d_model_via_images(input_image_paths, input_image_urls, bbox_condition)` - Generate 3D models from images
- `poll_rodin_job_status(subscription_key, request_id)` - Check generation status
- `import_generated_asset(name, task_uuid, request_id)` - Import generated assets

## Configuration

### Server Configuration

The server runs on `localhost:8000` by default. The Blender addon connects on port `9876`.

### Blender Addon Configuration

In Blender's BlenderMCP addon sidebar:

1. **Socket Settings**: Ensure server is running on port 9876
2. **PolyHaven**: Toggle to enable/disable integration
3. **Hyper3D**: Configure API mode and keys

## Workflow Examples

### Basic Scene Setup

```python
# Get current scene information
scene_info = get_scene_info()

# Execute code to create a basic object
code = """
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
"""
execute_blender_code(code)
```

### Using PolyHaven Assets

```python
# Check if PolyHaven is available
status = get_polyhaven_status()

# Search for textures
assets = search_polyhaven_assets("textures", "wood")

# Download and apply a texture
download_polyhaven_asset("wood_floor_01", "textures", "2k")
set_texture("Cube", "wood_floor_01")
```

### Using Hyper3D Generation

```python
# Check if Hyper3D is available
status = get_hyper3d_status()

# Generate a model from text
result = generate_hyper3d_model_via_text("a red sports car")
task_info = json.loads(result)

# Poll until completion
while True:
    status = poll_rodin_job_status(subscription_key=task_info["subscription_key"])
    if status == "Done":
        break

# Import the generated model
import_generated_asset("SportsCar", task_uuid=task_info["task_uuid"])
```

## Troubleshooting

### Connection Issues

- **"Could not connect to Blender"**: Ensure Blender is running with the BlenderMCP addon enabled
- **Socket timeout**: Large operations may take time; consider breaking them into smaller steps

### PolyHaven Issues

- **"PolyHaven integration is disabled"**: Enable it in the Blender addon sidebar
- **Download failures**: Check internet connection and PolyHaven service status

### Hyper3D Issues

- **"Insufficient balance"**: Free trial keys have daily limits
- **Generation failures**: Ensure prompts are clear and in English for text mode

## File Structure

```
Blender_MCP_check/
├── server.py              # Main MCP server
├── client_sse.py          # Test client
├── README.md              # This file
└── blender_addon/         # BlenderMCP addon files (separate)
```

## API Reference

### Asset Creation Strategy

The server follows a preferred strategy for creating 3D content:

1. **Check integrations**: Always verify PolyHaven and Hyper3D availability first
2. **Use external assets**: Prefer downloading from PolyHaven when suitable assets exist
3. **Generate custom assets**: Use Hyper3D for unique 3D models
4. **Fall back to scripting**: Only use manual Blender scripting when other methods fail

### Error Handling

All tools return descriptive error messages when operations fail. Common patterns:

- Connection errors indicate Blender addon issues
- "Integration disabled" means the feature needs to be enabled in Blender
- Timeout errors suggest operations should be simplified

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both server and client
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section
- Verify Blender addon is properly configured
- Ensure all prerequisites are installed
