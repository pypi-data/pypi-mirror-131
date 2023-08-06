from ...core.session import PlatformSession
from ...delivery.data import Endpoint

NEWS_UNDERLYING_PLATFORM_KEY = "apis.data.news.underlying-platform"


class NewsEndpoint(Endpoint):
    def _get_url_root(self):
        underlying_platform = (
            self.session.config.get(NEWS_UNDERLYING_PLATFORM_KEY) or "rdp"
        )
        if underlying_platform not in {"rdp", "udf"}:
            message = (
                f"Not correct value for '{NEWS_UNDERLYING_PLATFORM_KEY}'. "
                "Possible values: 'udf', 'rdp'"
            )
            self.session.error(message)
            raise ValueError(message)

        url = self.session._get_rdp_url_root()

        if underlying_platform == "udf":
            if isinstance(self.session, PlatformSession):
                self.session.warning(
                    "UDF News service cannot be used with platform sessions. "
                    f"The '{NEWS_UNDERLYING_PLATFORM_KEY} = 'udf' parameter "
                    "will be discarded, meaning that the regular RDP News service "
                    "will be used for News Story and News Headlines data requests."
                )
            else:
                url = self.session._get_udf_url()

        return url
