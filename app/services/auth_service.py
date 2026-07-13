from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
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
            hashed_password
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

    def register_user(
        self,
        user: User,
    ):

        user.password_hash = self.hash_password(
            user.password_hash
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
            return None

        if not self.verify_password(
            password,
            user.password_hash,
        ):
            return None

        token = self.create_access_token(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }