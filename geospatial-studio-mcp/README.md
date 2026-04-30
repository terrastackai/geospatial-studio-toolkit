# 🌍 Geospatial Studio MCP Server

A Model Context Protocol (MCP) server that provides AI assistants like Claude with direct access to IBM's Geospatial Studio platform. This server enables natural language interactions for geospatial AI model inference, fine-tuning, and data discovery.

## 📋 Overview

The Geospatial Studio MCP server exposes a comprehensive set of tools that allow AI assistants to:

- **🤖 Run AI Model Inference**: Submit and monitor geospatial AI model inference runs on satellite imagery
- **🎯 Fine-tune Models**: Create and manage custom model fine-tuning tasks
- **🔍 Discover Data**: Search and preview geospatial data from multiple sources using TerraKit
- **📍 Geocoding**: Convert location names to geographic coordinates and bounding boxes

## ✨ Features

### 🤖 Inference Tools
- `list_available_models()` - Browse available geospatial AI models
- `submit_inference_run()` - Run inference on a specific location and time period
- `list_inference_runs()` - View past inference runs
- `get_inference_run()` - Get detailed information about a specific run
- `get_inference_run_url()` - Get the UI URL for viewing results

### 🎯 Fine-tuning Tools
- `list_tuning_templates()` - View available task templates (segmentation, detection, etc.)
- `list_available_backbones()` - Browse foundation model backbones
- `list_tuning_datasets()` - View available training datasets
- `submit_fine_tuning_task()` - Start a new fine-tuning job
- `list_tunes()` - View all fine-tuning tasks
- `get_tune_details()` - Get status and details of a tuning task
- `get_tune_log()` - Retrieve training logs

### 🛰️ Data Discovery Tools (TerraKit)
- `terrakit_list_connectors()` - List available data sources
- `terrakit_collection_details()` - Get metadata about data collections
- `terrakit_find_data()` - Search for satellite imagery by location and date
- `preview_data()` - Generate preview images of satellite data

### 🗺️ Geospatial Utilities
- `get_location_bounding_box()` - Convert place names to coordinates

## 📦 Installation

### ✅ Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- An IBM Geospatial Studio account with API credentials
- Claude Desktop (for Claude Desktop integration)

### Step 1️⃣: Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Step 2️⃣: Install Dependencies

```bash
cd geospatial-studio-mcp
uv pip install -r requirements.txt
```

The required packages are:
- `terrakit` - Geospatial data discovery library
- `fastmcp` - MCP server framework
- `owslib` - Web Map Service client
- `geostudio` - IBM Geospatial Studio SDK

### Step 3️⃣: Configure API Credentials

Create a configuration file at `~/.geostudio-devstage-config` with your Geospatial Studio API credentials:

```json
{
  "api_key": "your-api-key-here",
  "api_url": "https://your-geostudio-instance.com/studio-gateway/"
}
```

**💡 Note**: Update the `api_key_filepath` variable in `geostudio-mcp.py` (line 26) if you want to use a different configuration file location.

## 🖥️ Setup in Claude Desktop

To use this MCP server with Claude Desktop, you need to add it to your Claude Desktop configuration file.

### macOS/Linux

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geostudio": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/geospatial-studio-mcp",
        "run",
        "geostudio-mcp.py"
      ]
    }
  }
}
```

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geostudio": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\absolute\\path\\to\\geospatial-studio-mcp",
        "run",
        "geostudio-mcp.py"
      ]
    }
  }
}
```

**⚠️ Important**: Replace `/absolute/path/to/` (or `C:\\absolute\\path\\to\\`) with the actual absolute path to your `geospatial-studio-mcp` directory.

**💡 Note**: Using `uv run` ensures the server runs with the correct dependencies isolated in a virtual environment, without needing to manually activate it.

### 🔄 Restart Claude Desktop

After updating the configuration file, restart Claude Desktop for the changes to take effect. You should see the MCP server tools available in Claude's interface.

## 💡 Example Use Cases

### Example 1: 🌊 Running Flood Detection Inference

```
User: "I need to detect flooding in Houston, Texas for the week of September 1-7, 2024 
using the flood detection model."

Claude will:
1. Use get_location_bounding_box() to find Houston's coordinates
2. Use list_available_models() to find the flood detection model
3. Use submit_inference_run() to start the inference
4. Provide the inference ID and URL to view results
```

### Example 2: 🛰️ Finding Satellite Imagery

```
User: "Show me recent Sentinel-2 imagery of the Amazon rainforest near Manaus from 
January 2024."

Claude will:
1. Use get_location_bounding_box() to get Manaus coordinates
2. Use terrakit_find_data() to search for Sentinel-2 data
3. Use preview_data() to generate a preview image
4. Display the image and available dates
```

### Example 3: 🎯 Fine-tuning a Model

```
User: "I want to fine-tune a model for detecting agricultural fields using the 
crop-segmentation dataset."

Claude will:
1. Use list_tuning_datasets() to find the crop-segmentation dataset
2. Use list_available_backbones() to show available foundation models
3. Use list_tuning_templates() to find the segmentation template
4. Use submit_fine_tuning_task() to start the fine-tuning job
5. Provide the tune ID and monitor progress with get_tune_details()
```

### Example 4: 📊 Monitoring Inference Progress

```
User: "What's the status of my recent inference runs?"

Claude will:
1. Use list_inference_runs() to show all your runs
2. Use get_inference_run() for detailed status of specific runs
3. Use get_inference_run_url() to provide links to view results in the UI
```

## 🛠️ Development

### 🚀 Running the Server Standalone

For testing purposes, you can run the server directly:

```bash
# Using uv (recommended)
uv run geostudio-mcp.py

# Or with standard Python
python geostudio-mcp.py
```

The server runs using stdio transport by default, which is suitable for MCP client integration.

### 🔌 Alternative Transport

The code includes a commented-out option for HTTP transport. To use it, modify the last line in `geostudio-mcp.py`:

```python
# Change from:
mcp.run(transport='stdio')

# To:
mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path='/mcp')
```

## 🔧 Troubleshooting

### ❌ Server Not Appearing in Claude Desktop

1. Check that the path in `claude_desktop_config.json` is absolute and correct
2. Verify Python is in your PATH
3. Check Claude Desktop logs for errors
4. Restart Claude Desktop after configuration changes

### 🔐 Authentication Errors

1. Verify your API credentials in the configuration file
2. Ensure the API URL is correct for your Geospatial Studio instance
3. Check that your API key has the necessary permissions

### 📚 Import Errors

1. Ensure all dependencies are installed: `uv pip install -r requirements.txt`
2. Verify you're using Python 3.8 or higher
3. Check that the geostudio SDK is properly installed
4. If using `uv run`, ensure you're in the correct directory

## 📖 Resources

- [IBM Geospatial Studio Documentation](https://terrastackai.github.io/geospatial-studio/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [TerraKit Documentation](https://github.com/IBM/terratorch)

## 📄 License

This project is part of the Geospatial Studio Toolkit. See the main repository LICENSE.txt for details.

