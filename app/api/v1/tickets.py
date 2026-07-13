from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ticket_service import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketResponse,
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = TicketService(db)

    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        user_id=current_user.id,
    )

    return service.create_ticket(ticket)