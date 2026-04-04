from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.database import Base, engine

# Import all models so SQLAlchemy registers them before create_all
import app.models.user      # noqa
import app.models.category  # noqa
import app.models.product   # noqa
import app.models.review    # noqa
import app.models.cart      # noqa
import app.models.wishlist  # noqa
import app.models.order     # noqa

from app.routers import auth, users, categories, products, cart, wishlist, orders, uploads


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup (dev convenience)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## 🛍️ Exclusive Shop — REST API (عربي)

واجهة برمجية كاملة لمتجر Exclusive الإلكتروني.

### الميزات
- **JWT Authentication** — تسجيل دخول + refresh token
- **Products** — بحث، فلترة، تقييمات
- **Cart** — إضافة / تعديل / حذف
- **Wishlist** — المفضلة
- **Orders** — Checkout + تتبع الطلبات
- **Admin** — إدارة المنتجات والفئات والمستخدمين

### بيانات الدخول التجريبية
| الدور | البريد | كلمة المرور |
|-------|--------|-------------|
| مشرف | admin@exclusive.com | Admin@123 |
| مستخدم | user@exclusive.com | User@1234 |
""",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
PREFIX = "/api/v1"
app.include_router(auth.router,       prefix=PREFIX)
app.include_router(users.router,      prefix=PREFIX)
app.include_router(categories.router, prefix=PREFIX)
app.include_router(products.router,   prefix=PREFIX)
app.include_router(cart.router,       prefix=PREFIX)
app.include_router(wishlist.router,   prefix=PREFIX)
app.include_router(orders.router,     prefix=PREFIX)
app.include_router(uploads.router,    prefix=PREFIX)


@app.get("/", tags=["🏠 Root"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running ✅",
    }


@app.get("/health", tags=["🏠 Root"])
def health():
    return {"status": "ok"}
