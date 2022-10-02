from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # Get user from DB based on email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Raise an error if it is not found
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Verify the password is correct
    if not utils.verify_password(user_credentials.password, user.password):
        # If the password is incorrect raise error
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Return a token
    access_token_expires = oauth2.token_expiration()
    access_token = oauth2.create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
