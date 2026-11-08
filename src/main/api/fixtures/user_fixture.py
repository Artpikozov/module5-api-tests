import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.fixture
def user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_account(api_manager, user_request):
    return api_manager.user_steps.create_account(user_request)

@pytest.fixture
def create_second_account(api_manager, user_request):
    return api_manager.user_steps.create_account(user_request)

@pytest.fixture
def create_user_credit(api_manager):
    credit_user_request = RandomModelGenerator.generate(CreateUserRequest)
    credit_user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(credit_user_request)
    return credit_user_request

@pytest.fixture
def create_credit_account(api_manager, create_user_credit):
    return api_manager.user_steps.create_account(create_user_credit)

@pytest.fixture
def repay_credit(api_manager,create_user_credit, create_credit_account):
    credit_request = CreditRequest(accountId=create_credit_account.id, amount= 5000, termMonths=12 )
    return api_manager.user_steps.credit_request(create_user_credit, credit_request)

@pytest.fixture
def deposit_first_account(api_manager, user_request, create_account):
    deposit_request = AccountDepositRequest(accountId=create_account.id, amount=5000)
    return api_manager.user_steps.deposit_account(user_request, deposit_request)

