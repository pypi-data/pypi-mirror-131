import json
from .request import ModexRequest


class UserManagement:

    def create(self, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/createUser',
            params, node_type="auth")

