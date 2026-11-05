from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)


#Casos faltantes para cumplir con lo que se pide la evidencia E6
def test_admin_cancels_other_user_order():
    """Un administrador cancela un pedido NEW de otro usuario (permitido)."""
    now = datetime.now(timezone.utc)
    assert can_cancel("NEW", owner_id=1, user_id=2, is_admin=True, created_at=now - timedelta(hours=5), now=now)

def test_owner_cancel_exactly_at_24h_denied():
    """El propietario intenta cancelar exactamente a las 24 horas (debe rechazarse)."""
    now = datetime.now(timezone.utc)
    assert not can_cancel("NEW", owner_id=1, user_id=1, is_admin=False, created_at=now - timedelta(hours=24), now=now)
