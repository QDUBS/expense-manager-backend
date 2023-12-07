from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from schemas.newsLetterList import NewsLetterListSchema, ShowNewsLetterList
from schemas.user import UserSchema
from models import newsLetterList
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/news-letter-list",
    tags=['News Letter List']
)


@router.get('/', response_model=List[ShowNewsLetterList], status_code=status.HTTP_200_OK)
def get_news_letter_list(user_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    news_letter_list = db.query(newsLetterList.NewsLetterList).filter(
        newsLetterList.NewsLetterList.user_id == user_id).all()

    return news_letter_list


@router.get('/{id}', response_model=ShowNewsLetterList, status_code=status.HTTP_200_OK)
def get_news_letter_list(id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    single_news_letter_list = db.query(newsLetterList.NewsLetterList).filter(
        newsLetterList.NewsLetterList.id == id).first()

    if not single_news_letter_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"News letter list with id of {id} does not exist.")

    return single_news_letter_list


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_news_letter_list(request: NewsLetterListSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_news_letter_list = newsLetterList.NewsLetterList(
        user_id=request.user_id, name=request.name, email=request.email)
    db.add(new_news_letter_list)
    db.commit()
    db.refresh(new_news_letter_list)

    return new_news_letter_list
