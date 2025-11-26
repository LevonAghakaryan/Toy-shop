# Իմպորտներ
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.responses import HTMLResponse
from typing import Optional

# Մոդուլների router-ների ներմուծում
from .modules.products.presentation.router import router as products_router
from .modules.category.presentation.router import router as category_router
from .modules.orders.presentation.router import router as orders_router
from .modules.cart.presentation.router import router as cart_router
from .modules.admin.presentation.router import router as admin_router
from .modules.users.presentation.router import router as user_router
from .modules.users.presentation.router import get_user_service # Իմպորտում ենք service-ը ստանալու համար
from .modules.users.application.services import UserService
from .modules.users.domain.schemas import User # Օգտատիրոջ սխեման

app = FastAPI(title="FOODMARKET")

# Static ֆայլերի միացում
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")
app.state.templates = templates

# -------------------------------------------------------------
# ՆՈՐ ԿԱԽՎԱԾՈՒԹՅՈՒՆ (DEPENDENCY)՝ ՕԳՏԱՏԻՐՈՋ ՏՎՅԱԼՆԵՐԸ ՍՏԱՆԱԼՈՒ ՀԱՄԱՐ
# -------------------------------------------------------------
def get_user_from_cookie(
    request: Request,
    service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Կարդում է 'user_id' cookie-ն և վերադարձնում մուտք գործած օգտատիրոջ տվյալները։"""
    user_id_str = request.cookies.get("user_id")
    if not user_id_str:
        return None
    try:
        user_id = int(user_id_str)
        # Օգտագործում ենք repository-ի ֆունկցիան՝ առանց HTTPException բարձրացնելու
        db_user = service.repository.get_by_id(user_id)
        if db_user:
            # Փոխակերպում ենք DB մոդելը Pydantic սխեմայի
            return User.model_validate(db_user)
        return None
    except (ValueError, HTTPException):
        # Սխալ ID ֆորմատ կամ օգտատերը գտնված չէ
        return None

# -------------------------------------------------------------
# UI-ի համար ռոուտերների թարմացում՝ user օբյեկտը փոխանցելու համար
# -------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def home(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Մեր Մենյուն", "user": user})

@app.get("/products/all_products", include_in_schema=False)
async def products_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    return templates.TemplateResponse("products/products.html", {"request": request, "title": "Մեր Մենյուն", "user": user})

# ՆՈՐ ՌՈՈՒՏԵՐՆԵՐ ԳՐԱՆՑՄԱՆ/ՄՈՒՏՔԻ ԷՋԵՐԻ ՀԱՄԱՐ
@app.get("/register", include_in_schema=False)
async def register_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    """Ցուցադրում է օգտատիրոջ գրանցման էջը։"""
    return templates.TemplateResponse("auth/register.html", {"request": request, "title": "Գրանցվել", "user": user})

@app.get("/login", include_in_schema=False)
async def login_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    """Ցուցադրում է օգտատիրոջ մուտքի էջը։"""
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "Մուտք", "user": user})

@app.get("/aboutus",include_in_schema=False)
async def about(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    return templates.TemplateResponse("aboutus/aboutus.html", {"request": request, "title": "Մեր մասին", "user": user})

@app.get("/cart", include_in_schema=False)
async def cart_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    """
    Բեռնում է cart.html էջը և ցուցադրում զամբյուղի պարունակությունը։
    """
    return templates.TemplateResponse("order_cart/cart.html", {"request": request, "title": "Զամբյուղ", "user": user})

# ԲԼՈԳԻ ԷՋԻ ՌՈՈՒՏԵՐ
@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    # Վերադարձնում է blog.html-ը
    return templates.TemplateResponse("blog/blog.html", {"request": request, "user": user})

# ԱԿՑԻԱՆԵՐԻ ԷՋԻ ՌՈՈՒՏԵՐ
@app.get("/akcianer", response_class=HTMLResponse)
async def actions_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    # Վերադարձնում է actions.html-ը
    return templates.TemplateResponse("akcianer/akcianer.html", {"request": request, "user": user})

@app.get("/kap", include_in_schema=False)
async def contact_page(request: Request, user: Optional[User] = Depends(get_user_from_cookie)):
    """
    Բեռնում է kap.html էջը (Կապ մեզ հետ)։
    """
    return templates.TemplateResponse("kap/kap.html", {"request": request, "title": "Կապ Մեզ Հետ", "user": user})

# API Router-ների միացում
app.include_router(products_router)
app.include_router(category_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(admin_router)
app.include_router(user_router)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)