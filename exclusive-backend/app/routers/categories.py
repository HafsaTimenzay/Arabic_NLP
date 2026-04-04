from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.category import Category
from app.schemas.product import CategoryOut
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/categories", tags=["📦 الفئات"])


class CategoryCreate(BaseModel):
    name:        str
    name_ar:     str
    slug:        str
    icon:        Optional[str] = None
    description: Optional[str] = None


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_active == True).all()


@router.get("/{slug}", response_model=CategoryOut)
def get_category(slug: str, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.slug == slug).first()
    if not cat:
        raise HTTPException(404, "الفئة غير موجودة")
    return cat


@router.post("/", response_model=CategoryOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    if db.query(Category).filter(Category.slug == payload.slug).first():
        raise HTTPException(400, "الـ slug مستخدم بالفعل")
    cat = Category(**payload.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}", dependencies=[Depends(get_current_admin)])
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "الفئة غير موجودة")
    db.delete(cat)
    db.commit()
    return {"message": "تم حذف الفئة"}
