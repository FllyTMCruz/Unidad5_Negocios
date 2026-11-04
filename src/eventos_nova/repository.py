"""Persistencia minima de Eventos Nova con SQLAlchemy."""

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from src.eventos_nova.domain import Evento


class EventosBase(DeclarativeBase):
    """Base declarativa propia del agregado de Eventos Nova."""


class EventoRow(EventosBase):
    """Fila persistida de un evento."""

    __tablename__ = "eventos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    total_proveedores: Mapped[int] = mapped_column(Integer, nullable=False)


class SqlEventoRepository:
    """Repositorio SQL para eventos, sin controlar el commit de la sesion."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, evento: Evento) -> None:
        """Agrega un evento a la sesion sin hacer commit."""
        self.session.add(
            EventoRow(
                id=evento.evento_id,
                total_proveedores=len(evento.proveedores),
            )
        )

    def get(self, evento_id: str) -> EventoRow | None:
        """Obtiene la fila de un evento o None si no existe."""
        return self.session.get(EventoRow, evento_id)


def make_engine(url: str = "sqlite+pysqlite:///:memory:"):
    """Crea un motor y las tablas del repositorio de eventos."""
    engine = create_engine(url)
    EventosBase.metadata.create_all(engine)
    return engine
