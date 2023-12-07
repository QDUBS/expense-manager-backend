from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from sqlalchemy.orm import Session
from schemas.profile import ProfileSchema, ShowProfile
from schemas.user import UserSchema
from models import profile
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/profiles",
    tags=['Profiles']
)


@router.get('/', response_model=List[ShowProfile], status_code=status.HTTP_200_OK)
def get_profiles(db: Session = Depends(get_db)):
    profiles = db.query(profile.Profile).all()

    return profiles


@router.get('/{id}', response_model=ShowProfile, status_code=status.HTTP_200_OK)
def get_profile(id: str, db: Session = Depends(get_db)):
    single_profile = db.query(profile.Profile).filter(
        profile.Profile.id == id).first()

    if not single_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with id of {id} does not exist.")

    return single_profile


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_profile(request: ProfileSchema, db: Session = Depends(get_db)):
    new_profile = profile.Profile(user_id=request.user_id, first_name=request.first_name, last_name=request.last_name, mobile_number=request.mobile_number,
                                  department=request.department, role=request.role, staff_id=request.staff_id, photo=request.photo)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_profile(id: str, request: ProfileSchema, db: Session = Depends(get_db)):
    single_profile = db.query(profile.Profile).filter(profile.Profile.id == id)
    if not single_profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with id of {id} does not exist.")

    single_profile.update({'user_id': request.user_id, 'first_name': request.first_name, 'last_name': request.last_name, 'mobile_number': request.mobile_number,
                           'department': request.department, 'role': request.role, 'staff_id': request.staff_id, 'photo': request.photo})
    db.commit()
    
    return "Updated"
