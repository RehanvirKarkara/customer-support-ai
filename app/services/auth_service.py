from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

class AuthService:
    """
    Handles all authentication related business logic.
    """

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, user_data: UserCreate) -> User:
        """
        Register a new Airtel customer.
        """

        # Check Customer ID
        existing_customer = self.user_repository.get_user_by_customer_id(
            user_data.customer_id
        )

        if existing_customer:
            raise ValueError("Customer ID already exists.")

        # Check Email
        existing_email = self.user_repository.get_user_by_email(
            user_data.email
        )

        if existing_email:
            raise ValueError("Email already registered.")

        # Hash Password
        hashed_password = hash_password(user_data.password)

        # Create User Model
        new_user = User(
            customer_id=user_data.customer_id,
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_password,
        )

        return self.user_repository.create_user(new_user)

    def login(self, email: str, password: str) -> str:
        """
        Login Airtel customer.
        Returns JWT Token.
        """

        user = self.user_repository.get_user_by_email(email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password.")

        token = create_access_token(
            data={
                "sub": str(user.id),
                "customer_id": user.customer_id,
                "email": user.email,
            }
        )

        return token

    def get_profile(self, user_id: int) -> User:
        """
        Return logged-in user's profile.
        """

        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        return user