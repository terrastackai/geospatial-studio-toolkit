![Geospatial Studio banner](../docs/images/banner.png)

# 🌍 GEOStudio Python SDK

<table>
<tr>
  <td><strong>License</strong></td>
  <td>
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" />
  </td>
</tr>
<tr>
  <td><strong>Distribution</strong></td>
  <td>

[![PyPI - Version](https://img.shields.io/pypi/v/geostudio)](https://pypi.org/project/geostudio/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/geostudio)](https://pypi.org/project/geostudio/)
  </td>
</tr>
<tr>
  <td><strong>TerraStackAI</strong></td>
  <td>
    <img src="https://img.shields.io/badge/TerraTorch-a3b18a" />
    <img src="https://img.shields.io/badge/TerraKit-588157" />
    <img src="https://img.shields.io/badge/Iterate-3a5a40" />
  </td>
</tr>
<tr>
  <td><strong>Built With</strong></td>
  <td>
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" />
    <img src=https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white />
    <image src=https://img.shields.io/badge/QGIS-Plugin-green?logo=qgis />
  </td>
</tr>
</table>

[![Studio Documentation](https://img.shields.io/badge/Studio_Documentation-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://terrastackai.github.io/geospatial-studio)

## 🚀 Overview

The **Geospatial Exploration and Orchestration Studio** is an integrated platform for **fine-tuning, inference, and orchestration of geospatial AI models**.  It combines a **no-code UI**, **low-code SDK**, and APIs to make working with geospatial data and AI accessible to everyone, from researchers to developers.

For interaction with the Geospatial Studio, in addition to the web-base UI and RESTful APIs, users can use the following tools (included in this repository):

* Python SDK
* QGIS plugin

These interfaces require access to a deployed instance of the Geospatial Studio, this could be remotely on a cluster, or a local deployment.  If you require more details about the Studio and how to deploy it, [see here](https://github.com/terrastackai/geospatial-studio).

## 🐍 Python SDK

The Geospatial Studio python SDK enables users to interface with the Geospatial Studio APIs in a more natural manner.

### Prerequisites

* Access Geospatial Studio deployment (this could be local, or remotely on a deployed cluster).

### Installation

1. Prepare a python 3.11+ environment, however you normally do that (e.g. conda, pyenv, poetry, etc.) and activate this new environment.

2. Install the Geospatial Studio SDK:

   ```Shell
   python -m pip install --upgrade pip
   pip install geostudio
   ```

### Authentication

Authentication to the Geospatial Studio is handled by a redirect in the UI, but for programmatic access (from the SDK, for example), the user will need to create an API key.  This is can be easily done through the UI.

1. Go to the Geospatial Studio UI page and navigate to the `Manage your API keys` link.

2. This should pop-up a window where you can generate, access and delete your api keys.  NB: every user is limited to a maximum of two activate api keys at any one time.

![Location of API key link](../docs/images/sdk-auth.png)

3. When you have generated an api key and you intend to use it for authentication through the python SDK, the best practice would be to store the API key and geostudio ui base url in a credentials file locally, for example in /User/bob/.geostudio_config_file. You can do this by:

    ```bash
    echo "GEOSTUDIO_API_KEY=<paste_api_key_here>" > .geostudio_config_file
    echo "BASE_STUDIO_UI_URL=<paste_ui_base_url_here>" >> .geostudio_config_file
    ```

### Example usage of the SDK

In your Python Interpreter:

```py
from geostudio import Client

# change the value of geostudio_config_file below to the path of the file you saved your config in
gfm_client = Client(geostudio_config_file=".geostudio_config_file")

# list available models in the studio
models = gfm_client.list_models()
print(models)

# list available tunes
tunes = gfm_client.list_tunes()
print(tunes)
```
