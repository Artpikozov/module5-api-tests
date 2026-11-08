import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager: ApiManager, user_request: CreateUserRequest, create_second_account, deposit_first_account: AccountDepositResponse, db_session: Session):
        transfer_request = AccountTransferRequest(fromAccountId=deposit_first_account.id, toAccountId=create_second_account.id , amount= 1000)

        transfer_response = api_manager.user_steps.transfer(user_request, transfer_request)

        assert transfer_response.toAccountId == transfer_request.toAccountId
        assert transfer_response.fromAccountId == transfer_request.fromAccountId
        assert transfer_response.fromAccountIdBalance == deposit_first_account.balance - transfer_request.amount

        sender_from_db = AccountCrudDb.get_account_by_id(db_session, deposit_first_account.id)
        assert sender_from_db.balance == deposit_first_account.balance - transfer_request.amount, 'С отправителя списана неверная сумма'

        receiver_from_db = AccountCrudDb.get_account_by_id(db_session, create_second_account.id)
        assert receiver_from_db.balance == create_second_account.balance + transfer_request.amount, 'Получателю пришла неверная сумма'

