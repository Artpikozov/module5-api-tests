import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects = []
    yield objects
    api_manager = ApiManager(objects)
    for obj in objects:
        if isinstance(obj, CreateUserResponse):
            api_manager.admin_steps.delete_user(obj.id)