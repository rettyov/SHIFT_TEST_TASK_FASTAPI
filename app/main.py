import sys
sys.path.append('/code/app')

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session

from auth import Auth
from database import engine, SessionLocal
from models import Base
from schemas import User, AuthModel
from crud import (
    get_user_by_employee_id,
    get_auth_user_by_username,
)
# добавим несколько записей для проверки
from create_db import create_db


create_db()

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBearer()
auth_handler = Auth()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/login')
def login(user_details: AuthModel, db: Session = Depends(get_db)):
    auth_user = get_auth_user_by_username(db, user_details)
    if auth_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username')
    if not auth_handler.verify_password(user_details.password, auth_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')
    access_token = auth_handler.encode_token(auth_user.username, auth_user.employee_id)
    _refresh_token = auth_handler.encode_refresh_token(auth_user.username, auth_user.employee_id)
    return {'access_token': access_token, 'refresh_token': _refresh_token}


@app.get('refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    _refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(_refresh_token)
    return {'access_token': new_token}


@app.get('/')
async def root():
    return 'Poop'


@app.get('/get-user-info', response_model=User)
def get_user_info(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    sub = auth_handler.decode_token(credentials.credentials)
    if not sub:
        raise HTTPException(status_code=401, detail='Invalid token')
    db_user = get_user_by_employee_id(db, sub)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user
