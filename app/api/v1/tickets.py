from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
)
from app.services.ticket_service import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


# -------------------------
# Create Ticket
# -------------------------
@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        status=TicketStatus.OPEN,
        user_id=current_user.id,
    )

    return service.create_ticket(ticket)


# -------------------------
# Get Ticket By ID
# -------------------------
@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    try:
        return service.get_ticket(ticket_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# -------------------------
# Get All Tickets
# -------------------------
@router.get(
    "/",
    response_model=list[TicketResponse],
)
def get_all_tickets(
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    return service.get_all_tickets()


# -------------------------
# Get Current User Tickets
# -------------------------
@router.get(
    "/me",
    response_model=list[TicketResponse],
)
def get_my_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    return service.get_user_tickets(current_user.id)


# -------------------------
# Update Ticket
# -------------------------
@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    try:
        return service.update_ticket(
            ticket_id,
            ticket_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# -------------------------
# Delete Ticket
# -------------------------
@router.delete(
    "/{ticket_id}",
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):

    service = TicketService(db)

    try:

        service.delete_ticket(ticket_id)

        return {
            "message": "Ticket deleted successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )