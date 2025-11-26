from fastapi import APIRouter, Depends, status, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

# Իմպորտներ մեր մոդուլից
from app.core.database import get_db
from ..application.services import UserService
from ..infrastructure.repositories import UserRepository
from ..domain.schemas import UserCreate, UserLogin, User

router = APIRouter(prefix="/users", tags=["User Management"])


# Կախվածություն (Dependency)՝ UserService-ը ստանալու համար
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


# --------------------- API Ծայրակետեր (Backend Logic) ---------------------

# 1. Գրանցում (Registration)
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_api(
        user_in: UserCreate,
        service: UserService = Depends(get_user_service)
):
    """Գրանցում է նոր օգտատիրոջը և վերադարձնում նրա տվյալները։"""
    return service.register_user(user_in)


# 2. Մուտք (Login)
@router.post("/login")
async def login_api(
        login_data: UserLogin,
        service: UserService = Depends(get_user_service)
):
    """
    Աուտենտիֆիկացնում է օգտատիրոջը, վերադարձնում է օգտատիրոջ ID-ն և դնում է Cookie։
    Նշում: Իրականում այստեղ պետք է ստեղծվի JWT, բայց պարզության համար դնում ենք User ID-ն Cookie-ի մեջ։
    """
    user = service.authenticate_user(login_data)

    # Պատրաստում ենք պատասխանը
    response = JSONResponse(
        content={"message": "Մուտքը հաջողությամբ կատարված է։", "user_id": user.id, "username": user.username},
        status_code=status.HTTP_200_OK
    )

    # Դնում ենք օգտատիրոջ ID-ն Cookie-ի մեջ (X-User-ID)
    response.set_cookie(
        key="user_id",
        value=str(user.id),
        httponly=True,
        samesite="lax",
        max_age=3600 * 24 * 7  # 1 շաբաթ
    )

    return response


# 3. Օգտատիրոջ տվյալները (Auth ստուգում)
@router.get("/me", response_model=User)
async def get_current_user_api(
        user_id: Optional[str] = Depends(lambda r: r.cookies.get("user_id")),
        service: UserService = Depends(get_user_service)
):
    """Վերադարձնում է մուտք գործած օգտատիրոջ տվյալները՝ հիմնվելով Cookie-ի վրա։"""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Աուտենտիֆիկացիա չի կատարվել։"
        )

    try:
        return service.get_user_by_id(int(user_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Սխալ օգտատիրոջ ID ձևաչափ։"
        )


# 4. Դուրս գալ (Logout)
@router.post("/logout")
async def logout_api():
    """Ջնջում է User ID Cookie-ն։"""
    response = JSONResponse(content={"message": "Դուրս եկաք համակարգից։"}, status_code=status.HTTP_200_OK)
    response.delete_cookie("user_id")
    return response


# --------------------- Օժանդակ Ֆունկցիա (Middleware ֆունկցիայի փոխարեն) ---------------------

def get_current_user_id(request: Request, service: UserService = Depends(get_user_service)) -> int:
    """
    Օգտագործվում է որպես Dependency՝ մուտք գործած օգտատիրոջ ID-ն ստանալու համար։
    """
    user_id_str = request.cookies.get("user_id")
    if not user_id_str:
        # Եթե Cookie-ն չկա, դա նշանակում է, որ օգտատերը մուտք չի գործել։
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Մուտք գործեք համակարգ՝ գործողությունը կատարելու համար։"
        )

    try:
        user_id = int(user_id_str)
        # Կարող ենք նաև ստուգել, արդյոք User-ը գոյություն ունի
        service.get_user_by_id(user_id)
        return user_id
    except (ValueError, HTTPException):
        # Եթե ID-ն սխալ է կամ User-ը գտնված չէ
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Աուտենտիֆիկացիայի սխալ։"
        )

