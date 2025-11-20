# Getting Started Guideline

## <a name='TableofContents'></a>Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Using GEOStudio SDK](#using-geofm-sdk)
  - [In Python Interpreter](#in-python-interpreter)
  - [Inference Example](#inference-example)
  - [Fine Tuning Example](#fine-tuning-example)
- [GeoFM Endpoints](#geofm-endpoints)

## <a name='Prerequisites'></a>Prerequisites

- `Python version >= 3.9`

## <a name='Installation'></a>Installation

Set up your virtual development environment with:

```bash
python -m venv venv

source venv/bin/activate
```

Download and install the SDK as well as the dependencies as follows:
```bash
pip install -e .
```
or install with dev, test and docs dependencies:
```bash
pip install -e ".[dev,test,docs]"
```

## <a name='UsingGeofmsdk'></a>Using GEOStudio SDK

There are examples and demos for use in your python modules or notebooks in the [`examples/`](../examples/) directory. You will need an api key to access the geofm models through the sdk.

After installing `geostudio`:

- Obtain your **GEOFM_API_KEY** by logging to the [GEOStudio UI](https://gfm.res.ibm.com/) and generating an API key.

- Next, create a `.env` file at the root of your project and copy the API key you generated into an environment variable named:

```ini
GEOFM_API_KEY=YOUR_GEOFM_API_KEY
```

### <a name='InPythonInterpreter'></a>In Python Interpreter

To use `geostudio`, you must have a `GEOFM_API_KEY` in your environment variables or pass it as a parameter when initializing the sdk client.
To initialize the client, you must specify the service that you intend to use:

```python
from geostudio import Client

GEOFM_API_KEY = os.getenv("GEOFM_API_KEY", None)
gfm_client = Client(api_key=GEOFM_API_KEY)
```

Next, you can now use the `gfm_client` to make requests to the GEOStudio API service.

### <a name='InferenceExample'></a>Inference Example

The example below, initializes the GEOStudio Client and lists available models that we can run inference jobs against.

```python
# Import the sdk client
from geostudio import Client

# You should have defined `GEOFM_API_KEY` as an env variable.
GEOFM_API_KEY = os.getenv("GEOFM_API_KEY", None)
# Instantiate the client.
gfm_client = Client(api_key=GEOFM_API_KEY)

models = gfm_client .list_models()
```

### <a name='FineTuningExample'></a>Fine Tuning Example

The example below, initializes the fine tuning client and lists available tunes.

```python
# Import the sdk client
from geostudio import Client

# You should have defined `GEOFM_API_KEY` as an env variable.
GEOFM_API_KEY = os.getenv("GEOFM_API_KEY", None)
# Instantiate the client.
gfm_client = Client(api_key=GEOFM_API_KEY)

tunes = gfm_client.list_tunes()
```

## <a name='GeoFMEndpoints'></a>GEOStudio Endpoints

The geostudio has support for the following APIs:

**Prod Stage**

- *Gateway API endpoint:* `https://gfm.res.ibm.com/studio-gateway/`
