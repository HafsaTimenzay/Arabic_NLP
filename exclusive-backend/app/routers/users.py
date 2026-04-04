from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin
from app.core.security import verify_password, hash_password
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, ChangePassword
from typing import List

router = APIRouter(prefix="/users", tags=["👤 المستخدمون"])


@router.get("/", response_model=List[UserOut], dependencies=[Depends(get_current_admin)])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    if current.id != user_id and not current.is_admin:
        raise HTTPException(403, "غير مصرح")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "المستخدم غير موجود")
    return user


@router.patch("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(current, field, value)
    db.commit()
    db.refresh(current)
    return current


@router.post("/me/change-password")
def change_password(payload: ChangePassword, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    if not verify_password(payload.current_password, current.password):
        raise HTTPException(400, "كلمة المرور الحالية غير صحيحة")
    current.password = hash_password(payload.new_password)
    db.commit()
    return {"message": "تم تغيير كلمة المرور بنجاح"}


@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "المستخدم غير موجود")
    db.delete(user)
    db.commit()
    return {"message": "تم حذف المستخدم"}
