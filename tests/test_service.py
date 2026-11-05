from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))

# Simulación con un mock de un timeout
def test_gateway_timeout():
    gateway = Mock()
    gateway.charge.side_effect = TimeoutError("Timeout de conexión")
    with pytest.raises(TimeoutError):
        OrderService(gateway).checkout(Order(100))
