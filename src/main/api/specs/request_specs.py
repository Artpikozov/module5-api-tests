from src.main.api.configs.config import Config
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
import requests


class RequestSpecs:

    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username,password=password)

        response = requests.post(
            url=f"{Config.fetch('backendUrl')}{Endpoint.LOGIN_USER.value.url}",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()

        )

        if response.status_code != 200:
            raise Exception(f"Failed to login: {response.status_code}{response.text}")

        token = LoginUserResponse(**response.json()).token

        headers = RequestSpecs.base_headers()
        headers["Authorization"] = f"Bearer {token}"
        return headers