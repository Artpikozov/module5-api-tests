from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):


    def create_account(self, user_request: CreateUserRequest) -> CreateAccountResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post()

        return response

    def deposit_account(self,user_request: CreateUserRequest, deposit_account_request):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(deposit_account_request)
        return response



    def deposit_account_invalid(self,user_request: CreateUserRequest, deposit_account_request):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(deposit_account_request)
        return response

    def credit_request(self, user_request: CreateUserRequest, credit_request: CreditRequest ) -> CreditResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created(),
        ).post(credit_request)
        return response

    def credit_request_invalid(self, user_request: CreateUserRequest, credit_request: CreditRequest, response_spec ) -> CreditResponse:
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.CREDIT_REQUEST,
            response_spec,
        ).post(credit_request)
        return response

    def repay_request(self, user_request: CreateUserRequest, repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok(),
        ).post(repay_request)
        return response

    def repay_request_invalid(self, user_request: CreateUserRequest, repay_request: CreditRepayRequest, response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.CREDIT_REPAY,
            response_spec,
        ).post(repay_request)
        return response

    def transfer(self,user_request: CreateUserRequest, transfer_request: AccountTransferRequest) -> AccountTransferResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response







