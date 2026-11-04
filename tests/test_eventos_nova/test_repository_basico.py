from sqlalchemy.orm import Session

from src.eventos_nova.domain import Evento
from src.eventos_nova.repository import SqlEventoRepository, make_engine


def test_repository_evento_commit():
    engine = make_engine()
    evento = Evento("evento-1")
    evento.asignar_proveedor("proveedor-1")
    evento.asignar_proveedor("proveedor-2")

    with Session(engine) as session:
        repositorio = SqlEventoRepository(session)
        repositorio.save(evento)
        session.commit()

        fila = repositorio.get("evento-1")
        assert fila is not None
        assert fila.total_proveedores == 2


def test_repository_evento_rollback():
    engine = make_engine()
    evento = Evento("evento-2")
    evento.asignar_proveedor("proveedor-1")

    with Session(engine) as session:
        repositorio = SqlEventoRepository(session)
        repositorio.save(evento)
        session.rollback()

        assert repositorio.get("evento-2") is None
