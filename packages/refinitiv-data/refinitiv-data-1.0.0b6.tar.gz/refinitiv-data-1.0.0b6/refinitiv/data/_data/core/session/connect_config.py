import collections
import pathlib
import urllib
from typing import TYPE_CHECKING, List

import validators

from ... import configure
from ...tools import urljoin

if TYPE_CHECKING:
    from ...configure import _RDPConfig

config = configure.get_config()
keys = configure.keys
StreamServiceInformation = collections.namedtuple(
    "StreamServiceInformation",
    ["scheme", "host", "port", "path", "data_formats", "location"],
)


def extract_service_info(service_item):
    endpoint = service_item.get("endpoint")
    port = service_item.get("port")
    data_format = service_item.get("dataFormat")
    transport = service_item.get("transport")
    location = service_item.get("location")

    endpoint_path = pathlib.Path(endpoint)

    host = str(endpoint_path.parts[0])
    if len(endpoint_path.parts) > 1:
        path = "/".join(endpoint_path.parts[1:])
    else:
        path = None
    return transport, host, port, path, data_format, location


def convert_stream(service_item, scheme) -> StreamServiceInformation:
    (
        transport,
        host,
        port,
        path,
        data_formats,
        location,
    ) = extract_service_info(service_item)

    return StreamServiceInformation(
        scheme=scheme,
        host=host,
        port=port,
        path=path,
        data_formats=data_formats,
        location=location,
    )


def get_stream_service_information_by_ws_url(
    endpoint_ws_url,
) -> StreamServiceInformation:
    websocket_url_parse = urllib.parse.urlparse(endpoint_ws_url)

    stream_service_information = StreamServiceInformation(
        scheme=websocket_url_parse.scheme,
        host=websocket_url_parse.hostname,
        port=websocket_url_parse.port,
        path=websocket_url_parse.path.lstrip("/"),
        data_formats=["unknown"],
        location=None,
    )

    return stream_service_information


async def get_stream_service_information_by_request(
    request_func, url, scheme
) -> List[StreamServiceInformation]:
    service_discovery_response = await request_func(url)
    service_discovery_response = service_discovery_response.json()
    services = service_discovery_response.get("services", [])
    stream_service_information = [
        convert_stream(service, scheme)
        for service in services
        if service.get("transport") == "websocket"
    ]
    return stream_service_information


def get_discovery_endpoint_url(
    root_url: str, streaming_name: str, endpoint_name: str
) -> str:
    config_name = f"apis.streaming.{streaming_name}"
    config_endpoint_name = f"{config_name}.endpoints.{endpoint_name}"
    base_path = config.get_str(f"{config_name}.url")
    endpoint_path = config.get_str(f"{config_endpoint_name}.path")

    url = None
    base_path = base_path.strip()
    if base_path.startswith("/"):
        url = urljoin(root_url, base_path)

    elif validators.url(base_path):
        url = base_path

    url = urljoin(url, endpoint_path)
    return url


def filter_stream_services_by_location(locations, stream_service_information) -> list:
    if not locations:
        return stream_service_information

    #   build the prefer stream services
    prefer_stream_service_infos = []
    for prefer_stream_service_location in locations:
        for stream_service in stream_service_information:
            has_location = any(
                location.strip().startswith(prefer_stream_service_location)
                for location in stream_service.location
            )
            if has_location:
                prefer_stream_service_infos.append(stream_service)

    return prefer_stream_service_infos


async def get_desktop_stream_service_information(
    discovery_endpoint_url, endpoint_websocket_url, request_func
) -> List[StreamServiceInformation]:
    if endpoint_websocket_url is not None:
        return [get_stream_service_information_by_ws_url(endpoint_websocket_url)]
    scheme = "ws"
    stream_service_information = await get_stream_service_information_by_request(
        request_func, discovery_endpoint_url, scheme
    )
    return stream_service_information


async def get_platform_stream_service_information(api, request_func, url_root):
    _, streaming_name, endpoint_name = api.split("/")
    discovery_endpoint_url = get_discovery_endpoint_url(
        url_root, streaming_name, endpoint_name
    )

    endpoint_websocket_url = config.get(
        keys.get_stream_websocket_url(streaming_name, endpoint_name)
    )
    if endpoint_websocket_url is not None:
        return [get_stream_service_information_by_ws_url(endpoint_websocket_url)]

    scheme = "wss"
    stream_service_information = await get_stream_service_information_by_request(
        request_func, discovery_endpoint_url, scheme
    )

    locations = configure.get(
        keys.stream_connects_locations(streaming_name, endpoint_name)
    )

    stream_service_information = filter_stream_services_by_location(
        locations, stream_service_information
    )
    return stream_service_information


def get_deployed_stream_service_information(
    deployed_platform_host, session_name
) -> StreamServiceInformation:
    if deployed_platform_host is not None:
        scheme = "ws"
        (
            host,
            port,
        ) = deployed_platform_host.split(":")
    else:
        realtime_distribution_system_url_key = (
            f"{configure.keys.platform_realtime_distribution_system(session_name)}.url"
        )
        realtime_distribution_system_url = configure.get_str(
            realtime_distribution_system_url_key
        )
        realtime_distribution_system_url_parse = urllib.parse.urlparse(
            realtime_distribution_system_url
        )
        scheme = realtime_distribution_system_url_parse.scheme
        host = realtime_distribution_system_url_parse.hostname
        port = realtime_distribution_system_url_parse.port

    stream_service_information = StreamServiceInformation(
        scheme=scheme,
        host=host,
        port=port,
        path=None,
        data_formats=["tr_json2"],
        location=None,
    )
    return stream_service_information
