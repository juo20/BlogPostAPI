from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # Retrieve all posts from DB
    if limit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot search for less than 1 post")

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
        group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).\
        limit(limit).\
        offset(skip).\
        all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")

    return posts


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):

    # Get post by filtering for the ID and return 404 if not found
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"
        )

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: schemas.CurrentUser = Depends(get_current_user)):

    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, payload: schemas.Post, db: Session = Depends(get_db), current_user: schemas.CurrentUser = Depends(get_current_user)):
    """
    First the post will be queried according to the entered ID in the URL,
    if there is no corresponding post 404 will be returned, otherwise the
    ownership will be verified. If the user is the post owner the post will
    be updated and otherwise 401 returned.
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"
        )

    ownership = True if post.owner_id == current_user.id else False

    if not ownership:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not authorized to update post {id}"
        )

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.CurrentUser = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"
        )

    ownership = True if post.owner_id == current_user.id else False

    if not ownership:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not authorized to delete post {id}"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
