from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket import TicketUpdate


class TicketService:

    def __init__(self, db: Session):
        self.ticket_repository = TicketRepository(db)
        self.user_repository = UserRepository(db)

    # -------------------------
    # Create Ticket
    # -------------------------

    def create_ticket(
        self,
        ticket: Ticket,
    ) -> Ticket:

        # Verify that the user exists
        user = self.user_repository.get_user_by_id(ticket.user_id)

        if user is None:
            raise ValueError("User not found.")

        return self.ticket_repository.create_ticket(ticket)

    # -------------------------
    # Get Ticket
    # -------------------------

    def get_ticket(
        self,
        ticket_id: int,
    ) -> Ticket:

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found.")

        return ticket

    # -------------------------
    # Get All Tickets
    # -------------------------

    def get_all_tickets(self):

        return self.ticket_repository.get_all_tickets()

    # -------------------------
    # Get User Tickets
    # -------------------------

    def get_user_tickets(
        self,
        user_id: int,
    ):

        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        return self.ticket_repository.get_user_tickets(user_id)

    # -------------------------
    # Update Ticket
    # -------------------------

    def update_ticket(
        self,
        ticket_id: int,
        ticket_data: TicketUpdate,
    ) -> Ticket:

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found.")

        update_data = ticket_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(ticket, field, value)

        return self.ticket_repository.update_ticket(ticket)

    # -------------------------
    # Delete Ticket
    # -------------------------

    def delete_ticket(
        self,
        ticket_id: int,
    ):

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found.")

        self.ticket_repository.delete_ticket(ticket)