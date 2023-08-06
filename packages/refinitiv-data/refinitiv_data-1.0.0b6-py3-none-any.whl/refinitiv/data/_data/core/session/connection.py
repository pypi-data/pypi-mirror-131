import abc

from . import connect_config
from .auth_manager import AuthManager
from .stream_service_discovery.stream_connection_configuration import (
    RealtimeDistributionSystemConnectionConfiguration,
    DesktopStreamConnectionConfiguration,
)
from ... import configure
from ...errors import PlatformSessionError

config = configure.get_config()
keys = configure.keys


class SessionConnection(abc.ABC):
    def __init__(self, session):
        self._session = session

        self.log = session.log
        self.debug = session.debug

    async def get_stream_connection_configuration(self, stream_connection_name: str):
        pass

    async def open(self) -> bool:
        pass

    def close(self):
        pass

    def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        auth=None,
        loop=None,
        **kwargs,
    ):
        pass

    def get_omm_login_message(self):
        pass


class PlatformConnection(SessionConnection, abc.ABC):
    pass


class RefinitivDataConnection(PlatformConnection):
    def __init__(self, session):
        PlatformConnection.__init__(self, session)
        self.auth_manager = AuthManager(session, auto_reconnect=session.server_mode)

    def get_omm_login_message(self) -> dict:
        return {
            "NameType": "AuthnToken",
            "Elements": {
                "AuthenticationToken": self._session._access_token,
                "ApplicationId": self._session._dacs_params.dacs_application_id,
                "Position": self._session._dacs_params.dacs_position,
            },
        }

    async def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        auth=None,
        loop=None,
        **kwargs,
    ):
        return await self._session._http_request_async(
            url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            auth=auth,
            loop=loop,
            **kwargs,
        )

    async def get_stream_connection_configuration(
        self, api: str
    ) -> RealtimeDistributionSystemConnectionConfiguration:
        _, streaming_name, endpoint_name = api.split("/")
        protocols = configure.get_list(
            keys.stream_protocols(streaming_name, endpoint_name)
        )

        stream_service_information = (
            await connect_config.get_platform_stream_service_information(
                api, self._session.http_request_async, self._session._get_rdp_url_root()
            )
        )

        return RealtimeDistributionSystemConnectionConfiguration(
            self._session,
            stream_service_information,
            protocols,
        )

    async def open(self) -> bool:
        return await self.auth_manager.authorize()

    def close(self):
        self.debug("Close platform session...")
        self.auth_manager.close()


class DeployedConnection(PlatformConnection):
    def get_omm_login_message(self):
        return {
            "Name": self._session._dacs_params.deployed_platform_username,
            "Elements": {
                "ApplicationId": self._session._dacs_params.dacs_application_id,
                "Position": self._session._dacs_params.dacs_position,
            },
        }

    async def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        auth=None,
        loop=None,
        **kwargs,
    ):
        raise PlatformSessionError(
            -1,
            "Error!!! Platform session cannot connect to refinitiv dataplatform. "
            "Please check or provide the access right.",
        )

    async def get_stream_connection_configuration(
        self, stream_connection_name: str
    ) -> RealtimeDistributionSystemConnectionConfiguration:
        stream_service_information = (
            connect_config.get_deployed_stream_service_information(
                self._session._deployed_platform_host, self._session.name
            )
        )

        return RealtimeDistributionSystemConnectionConfiguration(
            self._session,
            [
                stream_service_information,
            ],
            [
                "OMM",
            ],
        )


class RefinitivDataAndDeployedConnection(DeployedConnection, RefinitivDataConnection):
    def __init__(self, session):
        DeployedConnection.__init__(self, session)
        RefinitivDataConnection.__init__(self, session)

    async def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        auth=None,
        loop=None,
        **kwargs,
    ):
        return await RefinitivDataConnection.http_request_async(
            self,
            url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            auth=auth,
            loop=loop,
            **kwargs,
        )

    async def get_stream_connection_configuration(
        self, stream_connection_name: str
    ) -> RealtimeDistributionSystemConnectionConfiguration:
        if stream_connection_name.startswith("streaming/pricing/main"):
            return await DeployedConnection.get_stream_connection_configuration(
                self, stream_connection_name
            )
        else:
            return await RefinitivDataConnection.get_stream_connection_configuration(
                self, stream_connection_name
            )

    async def open(self) -> bool:
        return await RefinitivDataConnection.open(self)

    def close(self):
        RefinitivDataConnection.close(self)


class DesktopConnection(SessionConnection):
    async def get_stream_connection_configuration(self, api: str):
        _, streaming_name, endpoint_name = api.split("/")
        discovery_endpoint_url = connect_config.get_discovery_endpoint_url(
            self._session._get_rdp_url_root(), streaming_name, endpoint_name
        )
        protocols = configure.get_list(
            keys.stream_protocols(streaming_name, endpoint_name)
        )
        endpoint_websocket_url = config.get(
            keys.get_stream_websocket_url(streaming_name, endpoint_name)
        )

        stream_service_information = (
            await connect_config.get_desktop_stream_service_information(
                discovery_endpoint_url,
                endpoint_websocket_url,
                self._session.http_request_async,
            )
        )

        stream_connection_configuration = DesktopStreamConnectionConfiguration(
            self._session,
            stream_service_information,
            protocols,
        )

        return stream_connection_configuration
