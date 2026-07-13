from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Handles all database operations related to users.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        """
        Save a new user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Get user using database ID.
        """
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_by_email(self, email: str) -> User | None:
        """
        Find user using email.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_user_by_customer_id(self, customer_id: str) -> User | None:
        """
        Find Airtel customer using Customer ID.
        """
        return (
            self.db.query(User)
            .filter(User.customer_id == customer_id)
            .first()
        )

    def get_all_users(self) -> list[User]:
        """
        Return all registered users.
        """
        return self.db.query(User).all()

    def update_user(self, user: User) -> User:
        """
        Save updated user information.
        """
        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user: User):
        """
        Delete user permanently.
        """
        self.db.delete(user)
        self.db.commit()