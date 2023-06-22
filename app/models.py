from sqlalchemy import Column, Integer, String, DATE, ForeignKey

from database import Base


class EmployeeDB(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    salary = Column(Integer)
    promotion = Column(DATE)


class AuthDB(Base):
    __tablename__ = 'logauth'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    employee_id = Column(ForeignKey('employee.employee_id'))
