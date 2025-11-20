# geofm-qgis-plugin

A QGIS plugin for managing(creating and visualizing) inferences

## Installation

#### Prerequisites

- python 3.8+
- pip package mamanger
- QGIS Long Term Release(LTR) version 3.40.5-Bratislava

<!-- #### Install from the Qgis python plugins repository -->
<!-- You can find the plug-in here: https://plugins.qgis.org/plugins/ -->

#### Install from source

``` bash
git clone git@github.com:terrastackai/geospatial-studio-toolkit.git
cd geospatial-studio-qgis

# create venv and activate it
python3 -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements-dev.txt
```

#### Deploy/ Install the plugin

``` bash
cd geo_inference
# run the deploy command
make deploy

```

#### Zip the plugin for distribution

```bash
cd geo_inference
## option 1: Zip the local dev version
## change version in metadata
make zip-local

## option 2: Zip the tested deployed version
## change version in metadata
make zip

## option for changing package name
## change plugin name in metadata or package name in makefile
PLUGINNAME = geo_inference # in makefile
PACKAGE_NAME = geostudio-qgis-plugin-$(VERSION) # in makefile
version=0.1 # in metadata.txt

```

### Install from Zip

#### Step 1: Open QGIS

Launch QGIS Desktop on your system.

#### Step 2: Access Plugin Manager

Navigate to **Plugins** → **Manage and Install Plugins** from the menu bar.

#### Step 3: Click Install from zip

![install screenshot1](./docs/images/256d3520-d7c7-4964-a64b-d5369114dd00.png)


#### Step 4: Add zip

Clone this repository

Add the path below:
```
path/geofm_qgis/geo_inference/package/geostudio-qgis-plugin-0.1.0.zip
```
![install screenshot2](./docs/images/c843a96e-575e-4262-a099-59bf7ccccbe9.png)

#### Step 5:Install and check the installed tab

Check the box  if not checked to enable the plugin:
![install screenshot3](./docs/images/58d9996b-037f-4050-8c13-297f971344d5.png)


#### How to make/view inferences

![2025-07-07 12-18-33](./docs/images/565da98e-f184-4c69-9eb2-b5a94985f71a.gif)

### Activating the plugin in QGIS

#### Step 1: Open QGIS

Launch QGIS Desktop on your system.

#### Step 2: Access Plugin Manager

Navigate to **Plugins** → **Manage and Install Plugins** from the menu bar.

#### Step 3: Locate the Plugin

1. Click on the **Installed** tab in the Plugin Manager dialog
2. Scroll through the list to find **IBM Geospatial Studio**
3. If you don't see it in the Installed tab, check the **All** tab to install it first

#### Step 4: Activate the Plugin

1. Check the box next to **IBM Geospatial Studio** to enable it
2. Click **Close** to exit the Plugin Manager

#### Step 5: Launch the Geo-Inference Tool

1. Look for the **geo_inference** icon in the QGIS toolbar
2. Click the icon to launch the plugin interface

**Note:** If you don't see the geo_inference icon after activation, try:
- Restarting QGIS
- Right-clicking on the toolbar and ensuring the plugin toolbar is visible
- Checking **View** → **Toolbars** to make sure all toolbars are enabled

### Usage

1. Insert API key
- Get the API Key got from the GEOStudio platform.

#### List inferences
- Click on list inferences button
- Click on one inference to see details
- Click load layer button to load layers from geoserver
- click add image to qgis to load layers from a presigned url

#### Submit inference
- **Load Models** and select the model
- select date start and end /or manually type the date
- Click **select area** button .This creates a layer and you can clcik on the map and draw a polygon
- click **submit inference**.

## Testing

This project includes a comprehensive unit test suite that can run without QGIS installation.

### Prerequisites

Install test dependencies:

```bash
pip install -r requirements-test.txt

# Navigate to the geo_inference directory
cd geo_inference

# Run all tests
make test

# Run tests with coverage
make test-coverage

## Direct pytest commands
# Basic test run
pytest

# With coverage
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_geo_inference_api.py

# Run with verbose output
pytest -v

```
