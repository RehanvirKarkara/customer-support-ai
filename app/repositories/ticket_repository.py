from sqlalchemy.orm import Session

from app.models.ticket import Ticket


class TicketRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_ticket(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get_ticket_by_id(self, ticket_id: int) -> Ticket | None:
        return (
            self.db.query(Ticket)
            .filter(Ticket.id == ticket_id)
            .first()
        )

    def get_all_tickets(self) -> list[Ticket]:
        return self.db.query(Ticket).all()

    def get_user_tickets(self, user_id: int) -> list[Ticket]:
        return (
            self.db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .all()
        )

    def update_ticket(self, ticket: Ticket) -> Ticket:
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def delete_ticket(self, ticket: Ticket) -> None:
        self.db.delete(ticket)
        self.db.commit()