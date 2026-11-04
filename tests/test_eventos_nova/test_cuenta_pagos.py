import pytest

from src.eventos_nova.domain import CuentaDePagos

# --- Casos de Exito ---


def test_exito_registrar_pago():
    cuenta = CuentaDePagos(saldo=0.0)
    nuevo_saldo = cuenta.registrar_pago(5000.0)
    assert nuevo_saldo == 5000.0
    assert cuenta.saldo == 5000.0


def test_exito_devolver_parcial():
    cuenta = CuentaDePagos(saldo=5000.0)
    monto_devuelto = cuenta.devolver(2000.0)
    assert monto_devuelto == 2000.0
    assert cuenta.saldo == 3000.0


def test_exito_calcular_devolucion_delegado():
    cuenta = CuentaDePagos(saldo=3000.0)
    monto_devuelto = cuenta.calcular_devolucion(1000.0)
    assert monto_devuelto == 1000.0
    assert cuenta.saldo == 2000.0


# --- Casos de Error ---


def test_error_saldo_inicial_negativo():
    with pytest.raises(ValueError, match="el saldo no puede ser negativo"):
        CuentaDePagos(saldo=-100.0)


def test_error_pago_no_positivo():
    cuenta = CuentaDePagos()
    with pytest.raises(ValueError, match="el monto debe ser positivo"):
        cuenta.registrar_pago(-50.0)

    with pytest.raises(ValueError, match="el monto debe ser positivo"):
        cuenta.registrar_pago(0.0)


def test_error_devolucion_excede_saldo():
    cuenta = CuentaDePagos(saldo=1000.0)
    with pytest.raises(ValueError, match="la devolucion no puede exceder el saldo"):
        cuenta.devolver(1500.0)


# --- Caso Limite ---


def test_limite_devolver_exactamente_todo_el_saldo():
    cuenta = CuentaDePagos(saldo=2500.0)
    monto = cuenta.devolver(2500.0)
    assert monto == 2500.0
    assert cuenta.saldo == 0.0