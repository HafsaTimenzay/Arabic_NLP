from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import Optional, List
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin
from app.models.product import Product
from app.models.review import Review
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, ProductListOut
from app.schemas.cart_wishlist_review import ReviewCreate, ReviewOut
import math

router = APIRouter(prefix="/products", tags=["🛍️ المنتجات"])


def _product_query(db: Session):
    return db.query(Product).options(joinedload(Product.category), joinedload(Product.reviews))


@router.get("/", response_model=ProductListOut)
def list_products(
    page:          int            = Query(1, ge=1),
    size:          int            = Query(12, ge=1, le=100),
    search:        Optional[str]  = None,
    category_id:   Optional[int]  = None,
    flash_sale:    Optional[bool] = None,
    featured:      Optional[bool] = None,
    min_price:     Optional[float]= None,
    max_price:     Optional[float]= None,
    sort:          str            = Query("newest", regex="^(newest|price_asc|price_desc|rating)$"),
    db:            Session        = Depends(get_db),
):
    q = _product_query(db).filter(Product.is_active == True)

    if search:
        term = f"%{search}%"
        q = q.filter(or_(Product.name.ilike(term), Product.name_ar.ilike(term)))
    if category_id:
        q = q.filter(Product.category_id == category_id)
    if flash_sale is not None:
        q = q.filter(Product.is_flash_sale == flash_sale)
    if featured is not None:
        q = q.filter(Product.is_featured == featured)
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)

    if sort == "price_asc":
        q = q.order_by(Product.price.asc())
    elif sort == "price_desc":
        q = q.order_by(Product.price.desc())
    elif sort == "rating":
        q = q.order_by(Product.created_at.desc())   # simplification
    else:
        q = q.order_by(Product.created_at.desc())

    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()

    return ProductListOut(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


@router.get("/flash-sales", response_model=List[ProductOut])
def flash_sales(limit: int = 8, db: Session = Depends(get_db)):
    return _product_query(db).filter(Product.is_flash_sale == True, Product.is_active == True).limit(limit).all()


@router.get("/featured", response_model=List[ProductOut])
def featured(limit: int = 8, db: Session = Depends(get_db)):
    return _product_query(db).filter(Product.is_featured == True, Product.is_active == True).limit(limit).all()


@router.get("/best-selling", response_model=List[ProductOut])
def best_selling(limit: int = 8, db: Session = Depends(get_db)):
    # Order by review count as proxy for popularity
    return (
        _product_query(db)
        .filter(Product.is_active == True)
        .outerjoin(Review)
        .group_by(Product.id)
        .order_by(func.count(Review.id).desc())
        .limit(limit)
        .all()
    )


@router.get("/related/{product_id}", response_model=List[ProductOut])
def related(product_id: int, limit: int = 4, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    q = _product_query(db).filter(Product.is_active == True, Product.id != product_id)
    if product.category_id:
        q = q.filter(Product.category_id == product.category_id)
    results = q.limit(limit).all()
    if len(results) < limit:
        extra = _product_query(db).filter(
            Product.is_active == True, Product.id != product_id,
            Product.id.notin_([r.id for r in results])
        ).limit(limit - len(results)).all()
        results.extend(extra)
    return results


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = _product_query(db).filter(Product.id == product_id).first()
    if not product or not product.is_active:
        raise HTTPException(404, "المنتج غير موجود")
    return product


@router.post("/", response_model=ProductOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if db.query(Product).filter(Product.slug == payload.slug).first():
        raise HTTPException(400, "الـ slug مستخدم بالفعل")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return _product_query(db).filter(Product.id == product.id).first()


@router.patch("/{product_id}", response_model=ProductOut, dependencies=[Depends(get_current_admin)])
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    return _product_query(db).filter(Product.id == product_id).first()


@router.delete("/{product_id}", dependencies=[Depends(get_current_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    product.is_active = False          # soft delete
    db.commit()
    return {"message": "تم حذف المنتج"}


# ── Reviews ─────────────────────────────────────────
@router.get("/{product_id}/reviews", response_model=List[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return [
        ReviewOut(
            id=r.id, rating=r.rating, title=r.title, body=r.body,
            created_at=r.created_at,
            user_name=r.user.name if r.user else "مجهول",
            user_avatar=r.user.avatar if r.user else None,
        )
        for r in reviews
    ]


@router.post("/{product_id}/reviews", response_model=ReviewOut, status_code=201)
def add_review(
    product_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    existing = db.query(Review).filter(Review.product_id == product_id, Review.user_id == current.id).first()
    if existing:
        raise HTTPException(400, "لقد قمت بتقييم هذا المنتج مسبقاً")
    review = Review(product_id=product_id, user_id=current.id, **payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return ReviewOut(
        id=review.id, rating=review.rating, title=review.title, body=review.body,
        created_at=review.created_at,
        user_name=current.name, user_avatar=current.avatar,
    )
