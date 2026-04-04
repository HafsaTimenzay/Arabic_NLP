"""
Seed script — populates the database with categories, products, and an admin user.
Run once:  python -m app.services.seed
"""
from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.product import Product

# Import all models so Base knows about them
import app.models.review     # noqa
import app.models.cart       # noqa
import app.models.wishlist   # noqa
import app.models.order      # noqa


CATEGORIES = [
    {"name": "Phones",       "name_ar": "الهواتف",       "slug": "phones",      "icon": "fa-mobile-alt"},
    {"name": "Computers",    "name_ar": "الحاسوب",       "slug": "computers",   "icon": "fa-laptop"},
    {"name": "SmartWatch",   "name_ar": "الساعات",       "slug": "smartwatch",  "icon": "fa-clock"},
    {"name": "Camera",       "name_ar": "الكاميرا",      "slug": "camera",      "icon": "fa-camera"},
    {"name": "HeadPhones",   "name_ar": "السماعات",      "slug": "headphones",  "icon": "fa-headphones"},
    {"name": "Gaming",       "name_ar": "الألعاب",       "slug": "gaming",      "icon": "fa-gamepad"},
    {"name": "Fashion",      "name_ar": "أزياء",         "slug": "fashion",     "icon": "fa-tshirt"},
    {"name": "Home",         "name_ar": "المنزل",        "slug": "home",        "icon": "fa-home"},
    {"name": "Sports",       "name_ar": "رياضة",         "slug": "sports",      "icon": "fa-running"},
    {"name": "Beauty",       "name_ar": "جمال",          "slug": "beauty",      "icon": "fa-spa"},
]

PRODUCTS = [
    {
        "name": "HAVIT HV-G92 Gamepad", "name_ar": "ذراع تحكم HAVIT HV-G92",
        "slug": "havit-hv-g92-gamepad",
        "description": "جهاز تحكم عالي الجودة مع لاصق هوائي للتثبيت السهل والإزالة الخالية من الفقاعات.",
        "price": 120, "old_price": 160, "stock": 50,
        "image": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=400&q=80",
        "images": [
            "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=600&q=80",
            "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=600&q=80",
        ],
        "colors": ["#4493F8", "#DB4444"], "sizes": ["XS", "S", "M", "L", "XL"],
        "badge": "-40%", "badge_type": "sale",
        "is_flash_sale": True, "is_featured": True, "category_slug": "gaming",
    },
    {
        "name": "AK-900 Wired Keyboard", "name_ar": "لوحة مفاتيح AK-900",
        "slug": "ak-900-wired-keyboard",
        "price": 960, "old_price": 1160, "stock": 35,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&q=80",
        "badge": "-35%", "badge_type": "sale", "is_flash_sale": True, "category_slug": "computers",
    },
    {
        "name": "IPS LCD Gaming Monitor", "name_ar": "شاشة ألعاب IPS LCD",
        "slug": "ips-lcd-gaming-monitor",
        "price": 370, "old_price": 400, "stock": 20,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&q=80",
        "badge": "-30%", "badge_type": "sale", "is_flash_sale": True, "category_slug": "computers",
    },
    {
        "name": "S-Series Comfort Chair", "name_ar": "كرسي S-Series مريح",
        "slug": "s-series-comfort-chair",
        "price": 375, "old_price": 400, "stock": 15,
        "image": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400&q=80",
        "badge": "-25%", "badge_type": "sale", "is_flash_sale": True, "category_slug": "home",
    },
    {
        "name": "The North Coat", "name_ar": "معطف نورث فيس",
        "slug": "the-north-coat",
        "price": 260, "old_price": 360, "stock": 40,
        "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&q=80",
        "is_featured": True, "category_slug": "fashion",
    },
    {
        "name": "Gucci Duffle Bag", "name_ar": "حقيبة غوتشي",
        "slug": "gucci-duffle-bag",
        "price": 960, "old_price": 1160, "stock": 10,
        "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&q=80",
        "is_featured": True, "category_slug": "fashion",
    },
    {
        "name": "RGB Liquid CPU Cooler", "name_ar": "مبرد CPU بالسائل RGB",
        "slug": "rgb-liquid-cpu-cooler",
        "price": 160, "old_price": 170, "stock": 60,
        "image": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?w=400&q=80",
        "is_featured": True, "category_slug": "computers",
    },
    {
        "name": "Small BookShelf", "name_ar": "رف كتب صغير",
        "slug": "small-bookshelf",
        "price": 360, "stock": 25,
        "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&q=80",
        "is_featured": True, "category_slug": "home",
    },
    {
        "name": "CANON EOS DSLR Camera", "name_ar": "كاميرا كانون DSLR",
        "slug": "canon-eos-dslr",
        "price": 360, "stock": 12,
        "image": "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&q=80",
        "category_slug": "camera",
    },
    {
        "name": "ASUS FHD Gaming Laptop", "name_ar": "لابتوب ASUS للألعاب",
        "slug": "asus-fhd-gaming-laptop",
        "price": 700, "old_price": 960, "stock": 18,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&q=80",
        "badge": "جديد", "badge_type": "new", "category_slug": "computers",
    },
    {
        "name": "Cosmology Product Set", "name_ar": "مجموعة منتجات التجميل",
        "slug": "cosmology-product-set",
        "price": 197, "stock": 80,
        "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&q=80",
        "category_slug": "beauty",
    },
    {
        "name": "Kids Electric Car", "name_ar": "سيارة كهربائية للأطفال",
        "slug": "kids-electric-car",
        "price": 960, "old_price": 1160, "stock": 7,
        "image": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400&q=80",
        "badge": "رائج", "badge_type": "new",
        "colors": ["#E00000", "#000000"], "category_slug": "home",
    },
    {
        "name": "Jr. Zoom Soccer Cleats", "name_ar": "حذاء كرة قدم Jr. Zoom",
        "slug": "jr-zoom-soccer-cleats",
        "price": 1160, "old_price": 1360, "stock": 30,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80",
        "colors": ["#FFD700", "#00CC00"], "category_slug": "sports",
    },
    {
        "name": "GP11 Shooter USB Gamepad", "name_ar": "ذراع تحكم GP11 Shooter",
        "slug": "gp11-shooter-usb-gamepad",
        "price": 660, "old_price": 1160, "stock": 22,
        "image": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=400&q=80",
        "badge": "-45%", "badge_type": "sale",
        "colors": ["#000000", "#333333"], "category_slug": "gaming",
    },
    {
        "name": "Quilted Satin Jacket", "name_ar": "جاكيت ساتان مبطن",
        "slug": "quilted-satin-jacket",
        "price": 660, "stock": 45,
        "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&q=80",
        "badge": "جديد", "badge_type": "new",
        "colors": ["#2F4F4F", "#000000"], "category_slug": "fashion",
    },
    {
        "name": "JBL Bluetooth Speaker", "name_ar": "سماعة JBL بلوتوث",
        "slug": "jbl-bluetooth-speaker",
        "price": 250, "old_price": 320, "stock": 55,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&q=80",
        "badge": "-22%", "badge_type": "sale", "category_slug": "headphones",
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Admin user
        if not db.query(User).filter(User.email == "admin@exclusive.com").first():
            db.add(User(
                name="المشرف",
                email="admin@exclusive.com",
                password=hash_password("Admin@123"),
                is_admin=True,
            ))
            db.add(User(
                name="مستخدم تجريبي",
                email="user@exclusive.com",
                password=hash_password("User@1234"),
            ))
            db.commit()
            print("✅ Users seeded")

        # Categories
        cat_map: dict[str, int] = {}
        for c in CATEGORIES:
            existing = db.query(Category).filter(Category.slug == c["slug"]).first()
            if not existing:
                obj = Category(**c)
                db.add(obj)
                db.flush()
                cat_map[c["slug"]] = obj.id
            else:
                cat_map[c["slug"]] = existing.id
        db.commit()
        print("✅ Categories seeded")

        # Products
        for p in PRODUCTS:
            if not db.query(Product).filter(Product.slug == p["slug"]).first():
                slug = p.pop("category_slug", None)
                p["category_id"] = cat_map.get(slug) if slug else None
                db.add(Product(**p))
        db.commit()
        print("✅ Products seeded")
        print("\n🎉 Database ready!")
        print("   Admin:  admin@exclusive.com / Admin@123")
        print("   User:   user@exclusive.com  / User@1234")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
