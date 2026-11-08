import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRequest:

    @pytest.mark.parametrize(
        'amount',
        [
            5000,
            15000
        ]
    )
    def test_credit_request(self, api_manager: ApiManager, create_user_credit: CreateUserRequest,
                            create_credit_account: CreateAccountResponse, db_session: Session, amount,):
        credit_request = CreditRequest(accountId=create_credit_account.id, amount=amount, termMonths=12)

        credit_response = api_manager.user_steps.credit_request(create_user_credit, credit_request)

        assert credit_request.amount == credit_response.amount
        assert credit_response.id == create_credit_account.id
        assert credit_response.creditId is not None
        assert credit_request.termMonths == credit_response.termMonths

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_credit_account.id)
        assert account_from_db.balance == create_credit_account.balance + amount, 'Сумма кредита не зачислена на счёт'
        assert credit_response.balance == account_from_db.balance

    @pytest.mark.parametrize(
        'amount, response_spec',
        [
            (4999, ResponseSpecs.request_bad()),
            pytest.param(
                15001, ResponseSpecs.request_unprocessable(),
                marks=pytest.mark.xfail(reason="По Swagger 422, фактически API отвечает 400", strict=True),
            ),
        ]
    )

    def test_credit_negative(self, api_manager: ApiManager, create_user_credit: CreateUserRequest,
                            create_credit_account: CreateAccountResponse, db_session: Session, amount, response_spec ):
        credit_request = CreditRequest(accountId=create_credit_account.id, amount=amount, termMonths=12)

        api_manager.user_steps.credit_request_invalid(create_user_credit, credit_request, response_spec)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_credit_account.id)
        assert account_from_db.balance == create_credit_account.balance, 'Деньги зачислены по невалидному кредиту'




    def test_credit_request_by_regular_user(self, api_manager: ApiManager, user_request: CreateUserRequest,
                            create_account: CreateAccountResponse, db_session: Session):
        credit_request = CreditRequest(accountId=create_account.id, amount=5000, termMonths=12)

        api_manager.user_steps.credit_request_invalid(user_request, credit_request, ResponseSpecs.request_forbidden())

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)
        assert account_from_db.balance == create_account.balance, 'Деньги зачислены по невалидному кредиту'



