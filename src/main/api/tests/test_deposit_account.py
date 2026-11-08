import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest




@pytest.mark.api
class TestDepositAccount:

    @pytest.mark.parametrize(
        "amount",
        [
            1000,
            9000
        ]
    )
    def test_deposit_account(self, api_manager: ApiManager, user_request: CreateUserRequest,
                             create_account: CreateAccountResponse, db_session: Session, amount):

        deposit_request = AccountDepositRequest(accountId=create_account.id, amount=amount)

        deposit_response = api_manager.user_steps.deposit_account(user_request, deposit_request)

        assert deposit_response.id == create_account.id
        assert deposit_response.balance == create_account.balance + deposit_request.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)
        assert account_from_db.balance == deposit_response.balance, "Баланс в БД не совпадает с ответом API"



    @pytest.mark.parametrize(
        "amount",
        [
            999,
            9001,
            0,
            -100,
        ]
    )
    def test_deposit_account_negativ(self, api_manager: ApiManager, user_request: CreateUserRequest,
                             create_account: CreateAccountResponse, db_session: Session, amount):
        deposit_request = AccountDepositRequest(accountId=create_account.id, amount=amount)

        deposit_response = api_manager.user_steps.deposit_account_invalid(user_request, deposit_request)


        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)
        assert account_from_db.balance == create_account.balance, "Баланс изменился после невалидного пополнения"

