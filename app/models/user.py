from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy.orm import relationship

class ServiceType(str, Enum):
    PREPAID = "PREPAID"
    POSTPAID = "POSTPAID"
    BROADBAND = "BROADBAND"
    DTH = "DTH"
    AIRTEL_BLACK = "AIRTEL_BLACK"


class CustomerType(str, Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    VIP = "VIP"


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    AGENT = "AGENT"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    mobile_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    service_type: Mapped[ServiceType] = mapped_column(
        SQLEnum(ServiceType),
        nullable=False,
    )

    customer_type: Mapped[CustomerType] = mapped_column(
        SQLEnum(CustomerType),
        default=CustomerType.REGULAR,
        nullable=False,
    )

    preferred_language: Mapped[str] = mapped_column(
        String(30),
        default="English",
    )

    circle: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.CUSTOMER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    
    tickets = relationship(
    "Ticket",
    back_populates="user",
    cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"customer_id='{self.customer_id}', "
            f"email='{self.email}')>"
        )