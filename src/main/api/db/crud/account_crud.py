from sqlalchemy.orm.session import Session

from src.main.api.db.models.account_table import Account

class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first() # .query это создание обьтекта запроса, с помощью которого мы можем получить данные из бд
                                        # filter_by нужен чтоб находить данные в таблице по заданному условию
                                        # .first() необходимо вернуть первый обьект, который удовлетворяет данному условию
    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commint()    #db.commint() тут точно удаляется аккаунт
