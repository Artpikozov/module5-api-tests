from sqlalchemy.orm.session import Session

from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first() # .query это создание обьтекта запроса, с помощью которого мы можем получить данные из бд
                                        # filter_by нужен чтоб находить данные в таблице по заданному условию
                                        # .first() необходимо вернуть первый обьект, который удовлетворяет данному условию

    @staticmethod
    def create_user_db(db: Session, username: str,password: str, role: str) -> User:
        user = User(
            username=username,
            password=password,
            role=role

        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
