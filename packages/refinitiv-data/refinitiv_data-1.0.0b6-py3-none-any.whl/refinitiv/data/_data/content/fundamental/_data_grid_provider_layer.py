from .data_grid_type import DataGridType
from .._content_provider import ContentProviderLayer
from ...core.session import get_valid_session, SessionType


class DataGridContentProviderLayer(ContentProviderLayer):
    async def get_data_async(self, session=None, on_response=None, **kwargs):
        """
        Returns a response asynchronously to the data platform

        Parameters
        ----------
        session : Session, optional
            Means default session would be used
        on_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        Response

        Raises
        ------
        AttributeError
            If user didn't set default session.

        """
        from .. import ContentType
        from ...delivery.data._data_provider import emit_event
        from ...delivery.data._data_provider_factory import get_url, get_api_config

        session = get_valid_session(session)
        config = session.config
        if (
            session.type == SessionType.PLATFORM
            and self._content_type == ContentType.DATA_GRID_UDF
        ):
            session.warning(
                f"UDF DataGrid service cannot be used with platform sessions. "
                f"The \"/apis/data/datagrid/underlying-platform = '{DataGridType.UDF.value}'\" "
                f"parameter will be discarded, meaning that the regular RDP DataGrid "
                f"service will be used for Fundamental and Reference data requests."
            )
            data_grid_config = get_api_config(ContentType.DATA_GRID_RDP, config)
            grid_config_items = data_grid_config.as_attrdict()
            layout = grid_config_items.get("layout", {}).get(DataGridType.RDP.value)
            self._kwargs["layout"] = layout

            self._initialize(ContentType.DATA_GRID_RDP, **self._kwargs)

        data_type = self._data_type
        url = get_url(data_type, config)
        api_config = get_api_config(data_type, config)
        auto_retry = api_config.get("auto-retry", False)
        response = await self._provider.get_data_async(
            session, url, auto_retry=auto_retry, **kwargs, **self._kwargs
        )
        on_response and emit_event(on_response, response, self, session)
        return response
