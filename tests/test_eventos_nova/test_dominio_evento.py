from datetime import UTC, datetime, timedelta

import pytest

from src.eventos_nova.domain import AsignacionProveedor, Evento

# --- Regla BR-15: Limite de 15 Proveedores ---


def test_exito_asignar_10_proveedores():
    evento = Evento(evento_id="EVT-01")
    for i in range(1, 11):
        evento.asignar_proveedor(f"PROV-{i}")
    assert len(evento.proveedores) == 10


def test_error_crear_evento_con_mas_de_15_proveedores():
    asignaciones = [AsignacionProveedor(f"PROV-{i}") for i in range(16)]
    with pytest.raises(
        ValueError, match="un evento no puede tener mas de 15 proveedores"
    ):
        Evento(evento_id="EVT-ERROR", asignaciones=asignaciones)


def test_limite_exacto_15_proveedores_y_desbordamiento_16():
    evento = Evento(evento_id="EVT-LIMITE")
    for i in range(1, 16):
        evento.asignar_proveedor(f"PROV-{i}")
    assert len(evento.proveedores) == 15

    # El proveedor 16 debe fallar por regla de negocio
    with pytest.raises(
        ValueError, match="un evento no puede tener mas de 15 proveedores"
    ):
        evento.asignar_proveedor("PROV-16")


# --- Regla BR-04: SLA de 48 Horas con Fechas Fijas UTC ---


def test_exito_sla_proveedor_a_las_24h():
    fecha_base = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
    asignacion = AsignacionProveedor(
        proveedor_id="PROV-01", fecha_asignacion=fecha_base
    )
    fecha_respuesta = fecha_base + timedelta(hours=24)

    cumple = asignacion.cofirmar(fecha=fecha_respuesta)
    assert cumple is True
    assert asignacion.evaluar_sla() is True


def test_limite_exacto_sla_48h():
    fecha_base = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
    asignacion = AsignacionProveedor(
        proveedor_id="PROV-LIM", fecha_asignacion=fecha_base
    )
    fecha_limite = fecha_base + timedelta(hours=48)

    cumple = asignacion.cofirmar(fecha=fecha_limite)
    assert cumple is True
    assert asignacion.evaluar_sla() is True


def test_limite_superado_sla_49h():
    fecha_base = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
    asignacion = AsignacionProveedor(
        proveedor_id="PROV-OUT", fecha_asignacion=fecha_base
    )
    fecha_tardia = fecha_base + timedelta(hours=49)

    cumple = asignacion.cofirmar(fecha=fecha_tardia)
    assert cumple is False
    assert asignacion.evaluar_sla() is False