from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AuthService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    # -------------------------
    # Password Hashing
    # -------------------------

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            hashed_password,
        )

    # -------------------------
    # JWT Token
    # -------------------------

    def create_access_token(
        self,
        user: User,
    ) -> str:

        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "customer_id": user.customer_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    # -------------------------
    # Register
    # -------------------------

    def register(
        self,
        user_data: UserCreate,
    ) -> User:

        # Check email
        if self.user_repo.get_user_by_email(user_data.email):
            raise ValueError("Email already registered.")

        # Check customer ID
        if self.user_repo.get_user_by_customer_id(
            user_data.customer_id
        ):
            raise ValueError("Customer ID already exists.")

        user = User(
            customer_id=user_data.customer_id,
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=self.hash_password(
                user_data.password
            ),
            mobile_number=user_data.mobile_number,
            service_type=user_data.service_type,
            customer_type=user_data.customer_type,
            preferred_language=user_data.preferred_language,
            circle=user_data.circle,
        )

        return self.user_repo.create_user(user)

    # -------------------------
    # Login
    # -------------------------

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.user_repo.get_user_by_email(email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not self.verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        return self.create_access_token(user)