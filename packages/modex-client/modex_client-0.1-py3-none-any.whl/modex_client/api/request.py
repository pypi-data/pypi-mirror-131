import os
import requests
from modex_client.utils import get_config_file


class ModexRequest:
    session = requests.Session()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = {
        "URI": os.getenv("MODEX_URI"),
        "DATA_PORTS": os.getenv("MODEX_DATA_PORTS"),
        "AUTH_PORTS": os.getenv("MODEX_AUTH_PORTS"),
        "TOKEN": os.getenv("MODEX_TOKEN"),
    }
    sys_config = get_config_file()

    def __init__(self, authenticated=False):
        if authenticated is True and self.sys_config is not None:
            self.session.headers.update(
                {"Authorization": "Bearer " + self.config["TOKEN"]}
            )

    def get_request(self, endpoint, node_type="data"):

        node_port = self.config["DATA_PORTS"]
        if node_type == "auth":
            node_port = self.config["AUTH_PORTS"]

        try:
            response = self.session.get(
                self.config["MODEX_URI"] + ":" + node_port + "/services" + endpoint
            )
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def post_request(self, endpoint, params, node_type="data"):
        data_params = params
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )

        node_port = self.config["DATA_PORTS"]
        if node_type == "auth":
            node_port = self.config["AUTH_PORTS"]
            self.session.headers.update({"Content-Type": "application/json"})
        try:
            response = self.session.post(
                self.config["URI"] + ":" + node_port + "/services" + endpoint,
                data=data_params,
                json=data_params,
            )
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
