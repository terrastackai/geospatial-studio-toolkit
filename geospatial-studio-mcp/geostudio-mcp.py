from typing import Any
import httpx
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import os

from geostudio import Client
from geopy.geocoders import Nominatim

from terrakit import DataConnector
from terrakit.download import geodata_utils
import requests

from owslib.wms import WebMapService
import requests
from pyproj import Transformer
# from PIL import Image
import PIL as pil
import io


# Initialize FastMCP server
mcp = FastMCP("geostudio-mcp")

api_key_filepath = '/Users/blair/.geostudio-devstage-config'

##############################################################################
#
#  Helper functions
#
###############################################################################


def bbox_to_pixel_size(bbox, resolution, src_crs='EPSG:4326', dst_crs='EPSG:3857'):
    """
    Convert bbox from src_crs to dst_crs and calculate pixel width/height for a given resolution.

    Args:
        bbox (tuple): (minx, miny, maxx, maxy) in src_crs
        resolution (float): spatial resolution in units of dst_crs (e.g., metres for EPSG:3857)
        src_crs (str): source CRS (default 'EPSG:4326')
        dst_crs (str): destination CRS (default 'EPSG:3857')

    Returns:
        (width_px, height_px): tuple of integers
        bbox_3857: transformed bbox in dst_crs
    """
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    minx, miny = transformer.transform(bbox[0], bbox[1])
    maxx, maxy = transformer.transform(bbox[2], bbox[3])
    bbox_3857 = (minx, miny, maxx, maxy)
    width_px = int(round((maxx - minx) / resolution))
    height_px = int(round((maxy - miny) / resolution))
    return width_px, height_px, bbox_3857

def _encode_image(image) -> ImageContent:
    """
    Encodes a PIL Image to a format compatible with ImageContent.
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_obj = Image(data=img_bytes, format="png")
    return img_obj.to_image_content()

##############################################################################
#
#  Geospatial Studio - Inferencing
#
###############################################################################

@mcp.tool()
def list_available_models() -> object:
    """
    Lists and returns the meta data about the available geospatial AI models in the Geospatial Studio.
    Returns:
        A list of the available models in the Geospatial Studio.
    """
    gfm_inference = Client(geostudio_config_file=api_key_filepath)
    models = gfm_inference.list_models(output="json")
    return models['results']

@mcp.tool()
def list_inference_runs() -> str:
    """
    Lists and returns the meta data about the past model inference runs the user has carried out in the Geospatial Studio.
    Returns:
        A list of the past user inference runs.
    """

    gfm_client = Client(geostudio_config_file=api_key_filepath)

    inference_runs = gfm_client.list_inferences()

    # remove the SLD body for size reasons
    for i in inference_runs['results']:
        if i['geoserver_layers'] is not None:
            if ('predicted_layers' in i['geoserver_layers']):
                for g in i['geoserver_layers']['predicted_layers']:
                    # print(g)
                    del g['sld_body']

    return inference_runs

@mcp.tool()
def submit_inference_run(model_display_name: str, description: str, location: str, bbox: list, date_range: str) -> str:
    """
    Submits an inference run in the Geospatial Studio, for a user requested location and time range for a particular AI model.
    Args:
        model_display_name: the name of the model to use for inference
        description: a short description of the inference run
        location: the location to run the inference over as a string
        bbox: the bounding box to run the inference over, in the format [lon_min, lat_min, lon_max, lat_max]
        date_range: the date range to run the inference over, in the format "YYYY-MM-DD" for a single date or "YYYY-MM-DD_YYYY-MM-DD" for a range
    Returns:
        A list of the past user inference runs.
    """

    gfm_client = Client(geostudio_config_file=api_key_filepath)

    request_payload = {
        "model_display_name": model_display_name,
        "description": description,
        "location": location,
        "spatial_domain": {
                "bbox": [bbox],
                "polygons": [],
                "tiles": [],
                "urls": []
        },
        "temporal_domain": [
                date_range
        ]
    }

    response = gfm_client.submit_inference(data=request_payload)

    return response

@mcp.tool()
def get_inference_run(inference_id: str) -> str:
    """
    Retrieves the details about a particular inference run in the Geospatial Studio.
    Args:
        inference_id: id of the inference run to get details for
    Returns:
        A json with a detailed information about the selected inference run
    """

    gfm_client = Client(geostudio_config_file=api_key_filepath)
    response = gfm_client.get_inference(inference_id=inference_id)

    return response

@mcp.tool()
def get_inference_run_url(inference_id: str) -> str:
    """
    Retrieves the URL to view the selected inference run in the Geospatial Studio UI.
    Args:
        inference_id: id of the inference run to get details for
    Returns:
        A URL for the inference page in the Geospatial Studio UI
    """

    gfm_client = Client(geostudio_config_file=api_key_filepath)
    response = gfm_client.get_inference(inference_id=inference_id)

    inference_url = gfm_client.api_url.replace("studio-gateway/","#inference?id=") + inference_id

    return inference_url

# @mcp.tool()
# def check_data_availability(data_connector: str, data_spec: dict) -> str:
#     """
#     Checks the availability of data in the Geospatial Studio.
#     Args:
#         datasource: 
#         data_spec:
#     Returns:
#         A json with a detailed information about the selected inference run
#     """

#     data_spec{
#         "collections": [
#             "string"
#         ],
#         "dates": [
#             "string"
#         ],
#         "bbox": [
#             [
#             0
#             ]
#         ],
#         "area_polygon": "string",
#         "maxcc": 0,
#         "pre_days": 1,
#         "post_days": 1
#         }

#     gfm_client = Client(geostudio_config_file=api_key_filepath)
#     response = gfm_client.check_data_availability(
#         datasource: data_connector,
#         data: data_spec,
#         output: str = "json",
#     )

#     return response


##############################################################################
#
#  Geospatial Studio - Fine-tuning
#
###############################################################################

@mcp.tool()
def list_tuning_templates() -> object:
    """
    Lists the tuning task templates available in the Geospatial Studio.  These represent the common
    types for the task, such as segmentation, regression, object detection.
    Returns:
        A list of the available tuning task templates in the Geospatial Studio.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    tasks = gfm_client.list_tune_templates(output="json")
    return tasks['results']

@mcp.tool()
def list_available_backbones() -> object:
    """
    Lists the available foundation model backbones in the Geospatial Studio.
    Returns:
        A list of the available model backbones in the Geospatial Studio.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    backbones = gfm_client.list_base_models(output="json")
    return backbones['results']

@mcp.tool()
def list_tuning_datasets() -> object:
    """
    Lists the fine-tuning datasets available in the Geospatial Studio.  These are the training 
    ready datasets which can be used to fine-tune the models.
    Returns:
        A list of the available fine-tuning ready datasets in the Geospatial Studio.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    datasets = gfm_client.list_datasets(output="json")
    return datasets['results']

@mcp.tool()
def tuning_template_details(task_id: str) -> object:
    """
    Lists and returns the detailed information about a particular tuning task template in the Geospatial Studio.
    This includes the information about the configurable hyperparameters and other details.
    Args:
        task_id: the tuning task template id
    Returns:
        A dictionary with the detailed information about the chosen tuning template.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    task_meta = gfm_client.get_task(task_id, output="json")
    return task_meta['results']


@mcp.tool()
def submit_fine_tuning_task(task_id: str,
                            dataset_id: str,
                            base_model_id: str,
                            tune_name: str,
                            tune_description: str) -> object:
    """
    Submit a fine-tuning task to the Geospatial Studio.
    Args:
        task_id: the tuning task template id
        dataset_id: id of the chosen dataset for fine-tuning
        base_model_id: id of the chosen model backbone
        name: a name for the fine-tuning task, must be lower case with no spaces
        description: a short description of the model being tuned.  usually containing information on the use-case.
    Returns:
        A dictionary with the details of the submitted tuning task.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)

    task_params = gfm_client.get_task_param_defaults(task_id)

    task_params['runner']['max_epochs'] = '2'
    task_params['optimizer']['type'] = 'AdamW'
    task_params['data']['batch_size'] = 4

    tune_payload = {
        "name": tune_name,
        "description": tune_description,
        "dataset_id": dataset_id,
        "base_model_id": base_model_id,
        "tune_template_id": task_id,
        "model_parameters": task_params # uncomment this line if you customised task_params in the cells above otherwise, defaults will be used
    }

    submitted = gfm_client.submit_tune(
            data = tune_payload,
            output = 'json'
    )

    return submitted

@mcp.tool()
def list_tunes() -> object:
    """
    Retrieves a list of the users tunes
    Returns:
        A dictionary with the status and detailed information about the chosen fine-tuning task.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    tunes = gfm_client.list_tunes(output='json')
    return tunes['results']


@mcp.tool()
def get_tune_details(tune_id: str) -> object:
    """
    Retrieves the details and status of the select tuning task.
    Args:
        tune_id: the tuning task id
    Returns:
        A dictionary with the status and detailed information about the chosen fine-tuning task.
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    tune_info = gfm_client.get_tune(tune_id, output='json')
    return tune_info

@mcp.tool()
def get_tune_log(tune_id: str) -> str:
    """
    Returns the log of the selected tuning task
    Args:
        tune_id: the tuning task id
    Returns:
        A string containing the log of the tuning task
    """
    gfm_client = Client(geostudio_config_file=api_key_filepath)
    tune_info = gfm_client.get_tune(tune_id, output='json')
    log_url = tune_info["logs_presigned_url"]

    try:
        response = requests.get(log_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Decode the content to a string
        log_content = response.text

        return log_content

    except requests.exceptions.RequestException as e:
        return f"Error fetching the file: {e}"



##############################################################################
#
#  Other geospatial
#
###############################################################################

@mcp.tool()
def get_location_bounding_box(location: str) -> dict:
    """
    Finds geolocation information for a given location name
    Args:
        location: Name of the location
    Returns:
        A dictionary including information on the geolocation of the place.
    """
    geolocator = Nominatim(user_agent="test_geostudio_agent")
    geolocation = geolocator.geocode(location)
    return geolocation.raw

##############################################################################
#
#  Geospatial Studio - TerraKit
#
###############################################################################

@mcp.tool()
def terrakit_find_data(data_connector: str, 
              collection_name: str, 
              date_start: str, 
              date_end: str, 
              bbox: list[float],
              bands: list = ["blue", "green", "red"]) -> dict:
    """
    Search for geospatial data using the TerraKit library.  It takes a location, data collection and date range.
    Args:
        data_connector: Name of the location
        collection_name: name of the data collection
        date_start: start date of the search window
        date_end: end date of the search window
        bbox: the bounding box to search in, in the format [lon_min, lat_min, lon_max, lat_max]
        bands: optional element specifying the bands desired
    Returns:
        A dictionary including information on the available data
    """
    data_connector = "sentinel_aws"
    dc = DataConnector(connector_type=data_connector)

    unique_dates, results = dc.connector.find_data(
        data_collection_name=collection_name,
        date_start=date_start,
        date_end=date_end,
        bands=bands,
        bbox=bbox
    )

    return results.to_dict()

@mcp.tool()
def terrakit_list_connector_collections(data_connector: str) -> list:
    """
    Lists the available data collections for a given data connector in the TerraKit geospatial data library.
    Args:
        data_connector: The name of the data connector
    Returns:
        A list of the available data collections for that data connector
    """
    dc = DataConnector(connector_type=data_connector)
    return dc.connector.list_collections()


@mcp.tool()
def terrakit_collection_details(data_connector: str = None) -> list:
    """
    Gives the detailed meta-data for data collections in the TerraKit geospatial data library.  
    You can optionally filter for a particular data connector.
    Args:
        data_connector: The name of the data connector (optional)
    Returns:
        A json with the detailed meta-data for data collections
    """
    return geodata_utils.load_and_list_collections(as_json=True, connector_type=data_connector)

@mcp.tool()
def terrakit_list_connectors() -> list:
    """
    Gives a list of available data connectors in the TerraKit geospatial data library.  
    Returns:
        A list of the available data connectors
    """
    cols = geodata_utils.load_and_list_collections(as_json=True)
    return list(set([X['connector'] for X in cols]))

@mcp.tool()
def preview_data(bbox: list,
                 date: str,
                 limit_resolution: bool = True
                 ) -> ImageContent:
    """
    Generates an image.
    Args:
        bbox: the bounding box to search in, as (lon_min, lat_min, lon_max, lat_max)
        date: the date of the image to retrieve, as 'YYYY-MM-DD'
        limit_resolution: whether to limit the resolution to a maximum size
    Returns:
        An image content object containing the image data.
    """

    max_dim = 1024

    # WMS server URL (example: NASA GIBS)
    wms_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi'

    # Connect to WMS
    wms = WebMapService(wms_url, version='1.3.0')

    # Parameters
    layer = 'HLS_S30_Nadir_BRDF_Adjusted_Reflectance'

    # Check if the layer exists in the WMS service
    if layer not in wms.contents:
        raise ValueError(f"Layer '{layer}' not found in WMS service. Available layers: {list(wms.contents.keys())}")

    resolution_m = 30  # 30 metres per pixel
    width, height, bbox_3857 = bbox_to_pixel_size(bbox, resolution_m)

    if limit_resolution==False:
        if width > max_dim or height > max_dim:
            scale = max(width / max_dim, height / max_dim)
            width = int(width / scale)
            height = int(height / scale)
            print(f"Rescaled to Width: {width} px, Height: {height} px")

    # GetMap request
    img = wms.getmap(
        layers=[layer],
        srs='EPSG:4326',
        bbox=bbox,
        size=[width, height],
        format='image/png',
        time=date
    )

    pil_img = pil.Image.open(io.BytesIO(img.read()))

    return _encode_image(pil_img)






if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path='/mcp')