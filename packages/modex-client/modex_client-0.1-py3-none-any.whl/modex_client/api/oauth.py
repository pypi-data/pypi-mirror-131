import json
from .request import ModexRequest
import os
import urllib
from modex_client.utils import save_config_file


class Authorization:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = {
        "CLIENT_ID": os.getenv("MODEX_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("MODEX_CLIENT_SECRET"),
    }

    def authorize(self) -> json:
        data_params = {}
        data_params.update(
            {
                "response_type": "code",
                "client_id": self.config["CLIENT_ID"],
                "redirect_uri": "https://bcdb.modex.tech/callback",
            }
        )
        modex_request = ModexRequest()
        # print('/oauth/authorize?' + urllib.parse.urlencode(data_params))
        token = modex_request.get_request(
            "/oauth/authorize?" + urllib.parse.urlencode(data_params)
        )
        # print(token)
        save_config_file(str(token))
        return token

    def generate_token(self, params) -> json:
        data_params = params.copy()
        data_params.update(
            {
                "client_id": self.config["CLIENT_ID"],
                "client_secret": self.config["CLIENT_SECRET"],
                "response_type": "code",
                "grant_type": "exchange_token",
            }
        )
        modex_request = ModexRequest()
        token = modex_request.post_request("/oauth/token", data_params)
        # print(token)
        save_config_file(str(token))
        return token