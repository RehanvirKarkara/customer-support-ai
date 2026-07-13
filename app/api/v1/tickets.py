from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
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
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    service = TicketService(db)

    try:
        return service.create_ticket(ticket)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


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
            status_code=404,
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
# Update Ticket
# -------------------------
@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
):
    service = TicketService(db)

    try:
        return service.update_ticket(ticket_id, ticket)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# -------------------------
# Delete Ticket
# -------------------------
@router.delete("/{ticket_id}")
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
            status_code=404,
            detail=str(e),
        )