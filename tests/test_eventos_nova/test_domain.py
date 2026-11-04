from datetime import UTC, datetime, timedelta

import pytest

from src.eventos_nova.domain import AsignacionProveedor, CuentaDePagos, Evento


def test_evento_rechaza_el_proveedor_numero_16():
    evento = Evento("evento-1")
    for proveedor in range(15):
        evento.asignar_proveedor(f"proveedor-{proveedor}")

    with pytest.raises(ValueError, match="15"):
        evento.asignar_proveedor("proveedor-16")


def test_asignacion_proveedor_cumple_sla_de_48_horas():
    asignada = datetime(2026, 1, 1, tzinfo=UTC)
    asignacion = AsignacionProveedor("proveedor-1", asignada)

    assert asignacion.evaluar_sla(asignada + timedelta(hours=48))
    assert not asignacion.evaluar_sla(asignada + timedelta(hours=48, seconds=1))


def test_cuenta_de_pagos_registra_pago_y_realiza_devolucion():
    cuenta = CuentaDePagos()

    cuenta.registrar_pago(1000)
    assert cuenta.devolver(250) == 250
    assert cuenta.saldo == 750
