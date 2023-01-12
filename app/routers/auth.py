from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, utils, models, oauth2
from ..database import get_db


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("", response_model=schemas.Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"invalid credentials",
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"invalid credentials",
        )

    # create and return JWT
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
