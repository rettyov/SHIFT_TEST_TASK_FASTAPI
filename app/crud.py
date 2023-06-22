from typing import Optional

from sqlalchemy.orm import Session

from models import EmployeeDB, AuthDB
from schemas import User, AuthModel


# Возможности авторизованного пользователя
def get_user_by_employee_id(db: Session, sub: str) -> Optional[User]:
    username, employee_id = sub
    return db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()


# Авторизация
def get_auth_user_by_username(db: Session, user_details: AuthModel) -> Optional[AuthDB]:
    return db.query(AuthDB).filter(AuthDB.username == user_details.username).first()
