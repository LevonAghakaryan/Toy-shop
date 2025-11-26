from fastapi import HTTPException, status
# Նորից ավելացնում ենք passlib-ը՝ sha256_crypt-ի համար
from passlib.context import CryptContext
from typing import Optional

# Իմպորտներ մեր մոդուլից
from ..infrastructure.repositories import UserRepository
from ..domain.schemas import UserCreate, UserLogin, User
from ..domain.models import User as UserModel  # Տվյալների բազայի մոդել

# Գաղտնաբառի հեշավորման կոնտեքստ՝ օգտագործելով թեթև sha256_crypt
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class UserService:
    """
    Օգտատիրոջ բիզնես տրամաբանության շերտ
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    # --- Գաղտնաբառի ֆունկցիաներ ---

    def get_password_hash(self, password: str) -> str:
        """
        Հեշավորում է տրված գաղտնաբառը՝ օգտագործելով sha256_crypt։
        Այս ալգորիթմը չունի 72 բայթի սահմանափակում և աշխատում է արագ։
        """
        # SHA256-ի համար կրճատում չի պահանջվում
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Ստուգում է, արդյոք տրված գաղտնաբառը համապատասխանում է հեշին։
        """
        return pwd_context.verify(plain_password, hashed_password)

    # --- CRUD ֆունկցիաներ ---

    def register_user(self, user_in: UserCreate) -> User:
        """
        Գրանցում է նոր օգտատիրոջ, նախ հեշավորելով գաղտնաբառը։
        """
        if self.repository.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Օգտատերն այդ էլեկտրոնային հասցեով արդեն գոյություն ունի։"
            )

        # Հեշավորում ենք գաղտնաբառը
        hashed_password = self.get_password_hash(user_in.password)

        db_user = self.repository.create_user(user_in, hashed_password)

        return User.model_validate(db_user)

    def authenticate_user(self, login_data: UserLogin) -> UserModel:
        """
        Աուտենտիֆիկացնում է օգտատիրոջը։
        """
        user = self.repository.get_by_email(login_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Սխալ էլ․ հասցե կամ գաղտնաբառ։"
            )

        # Ստուգում ենք գաղտնաբառը հեշավորված տարբերակով
        if not self.verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Սխալ էլ․ հասցե կամ գաղտնաբառ։"
            )

        return user

    def get_user_by_id(self, user_id: int) -> User:
        """Վերադարձնում է օգտատիրոջը ID-ով։"""
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Օգտատեր ID {user_id}-ով չի գտնվել։"
            )
        return User.model_validate(db_user)
