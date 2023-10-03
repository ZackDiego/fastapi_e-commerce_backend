from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from . import oauth2

router = APIRouter(
    tags = ["Authentication"]
)

# Login
@router.post('/login', status_code = status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):


    user = db.query(models.User).filter(models.User.username == user_credential.username).first()
    print(user)
    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    print(user_credential.password)

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }