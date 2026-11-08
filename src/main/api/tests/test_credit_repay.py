import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager: ApiManager, create_user_credit: CreateUserRequest, repay_credit: CreditResponse, db_session: Session):
        credit_repay = CreditRepayRequest(creditId=repay_credit.creditId, accountId=repay_credit.id, amount=repay_credit.amount)

        repay_response = api_manager.user_steps.repay_request(create_user_credit, credit_repay)

        assert repay_response.creditId == repay_credit.creditId
        assert repay_response.amountDeposited == credit_repay.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, repay_credit.id)
        assert account_from_db.balance == repay_credit.balance - credit_repay.amount, 'Сумма погашения не списалась со счёта'



    def test_credit_repay_invalid(self, api_manager: ApiManager, create_user_credit: CreateUserRequest,
                          repay_credit: CreditResponse, db_session: Session):

        credit_repay = CreditRepayRequest(creditId=repay_credit.creditId, accountId=repay_credit.id,
                                          amount=repay_credit.amount - 1000)

        repay_response = api_manager.user_steps.repay_request_invalid(create_user_credit, credit_repay, ResponseSpecs.request_unprocessable())


        account_from_db = AccountCrudDb.get_account_by_id(db_session, repay_credit.id)
        assert account_from_db.balance == repay_credit.balance, 'Баланс изменился после отклонённгого погашения'
