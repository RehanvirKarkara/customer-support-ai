from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository


class TicketService:

    def __init__(self, db: Session):
        self.ticket_repo = TicketRepository(db)

    def create_ticket(self, ticket: Ticket) -> Ticket:
        return self.ticket_repo.create_ticket(ticket)

    def get_ticket(self, ticket_id: int):
        return self.ticket_repo.get_ticket_by_id(ticket_id)

    def get_all_tickets(self):
        return self.ticket_repo.get_all_tickets()

    def update_ticket(self, ticket: Ticket):
        return self.ticket_repo.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int):
        return self.ticket_repo.delete_ticket(ticket_id)