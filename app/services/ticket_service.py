from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.schemas import ticket
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticket import TicketStatus


class TicketService:

    def __init__(self, db: Session):
        self.ticket_repository = TicketRepository(db)
        self.user_repository = UserRepository(db)

    def create_ticket(self, ticket: Ticket) -> Ticket:
        return self.ticket_repository.create_ticket(ticket)

    def get_ticket(self, ticket_id: int) -> Ticket:

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if not ticket:
            raise ValueError("Ticket not found.")

        return ticket

    def get_all_tickets(self):

        return self.ticket_repository.get_all_tickets()

    def get_user_tickets(self, user_id: int):

        return self.ticket_repository.get_user_tickets(user_id)

    def update_ticket(
        self,
        ticket_id: int,
        ticket_data: TicketUpdate,
    ) -> Ticket:

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if not ticket:
            raise ValueError("Ticket not found.")

        if ticket_data.title is not None:
            ticket.title = ticket_data.title

        if ticket_data.description is not None:
            ticket.description = ticket_data.description

        if ticket_data.priority is not None:
            ticket.priority = ticket_data.priority

        if ticket_data.status is not None:
            ticket.status = ticket_data.status

        return self.ticket_repository.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int):

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if not ticket:
            raise ValueError("Ticket not found.")

        self.ticket_repository.delete_ticket(ticket)