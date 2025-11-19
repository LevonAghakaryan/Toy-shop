# app/modules/admin/presentation/router.py (ՆՈՐ ՖԱՅԼ)
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

from app.core.database import get_db
from app.core.config import settings
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.products.application.services import ProductService
from app.modules.products.domain.schemas import ProductCreate
from app.modules.category.infrastructure.repositories import CategoryRepository
from app.modules.category.application.services import CategoryService

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")


def verify_admin_token(request: Request) -> dict:
    """Ստուգում է admin session-ը cookies-ից"""
    token = request.cookies.get("admin_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Նստաշրջումը ժամանականց է:",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.admin_secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Նստաշրջումը ժամանականց է՝ կրկին մուտք գացեք:"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Login էջի ցուցադրում"""
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.post("/login")
async def admin_login(request: Request):
    """Admin-ի մուտքի մշակում"""
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    # Ստուգում ենք credentials-ը
    if username == settings.admin_username and password == settings.admin_password:
        # JWT token-ի ստեղծում
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, settings.admin_secret_key, algorithm="HS256")

        response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="admin_token", value=token, httponly=True, max_age=86400)
        return response
    else:
        # Սխալ մուտք
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "error": "Մուտքի անուն կամ գաղտնաբառ սխալ"}
        )


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
        request: Request,
        admin: dict = Depends(verify_admin_token)
):
    """Admin dashboard էջ"""
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "username": admin["username"]}
    )


@router.get("/logout")
async def admin_logout():
    """Admin-ի հեռանցում"""
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("admin_token")
    return response


@router.post("/products/create")
async def admin_create_product(
        product_data: ProductCreate,
        db: Session = Depends(get_db),
        admin: dict = Depends(verify_admin_token)
):
    """API ռոուտ ապրանք ստեղծելու համար (միայն admin-ի համար)"""
    product_repo = ProductRepository(db)
    product_service = ProductService(product_repo)

    try:
        new_product = product_service.create_product(product_data)
        return {
            "success": True,
            "message": "Ապրանքը հաջողությամբ ստեղծվեց",
            "product": new_product
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


