from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    try:
        # Hashing user password before adding to DB
        user.password = utils.hash_password(user.password)

        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email {user.email} already exists")

    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    return user
