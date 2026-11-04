"""Entidades del dominio de Eventos Nova."""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass
class AsignacionProveedor:
    """Asignacion de un proveedor a un evento con SLA de cofirmacion de 48 horas."""

    proveedor_id: str
    fecha_asignacion: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    fecha_cofirmacion: datetime | None = None

    SLA_HORAS = 48

    @property
    def fecha_limite_sla(self) -> datetime:
        return self.fecha_asignacion + timedelta(hours=self.SLA_HORAS)

    def evaluar_sla(self, ahora: datetime | None = None) -> bool:
        """Indica si la cofirmacion ocurrio dentro del plazo de 48 horas."""
        referencia = self.fecha_cofirmacion or ahora or datetime.now(UTC)
        return referencia <= self.fecha_limite_sla

    def cofirmar(self, fecha: datetime | None = None) -> bool:
        """Registra la cofirmacion y devuelve si cumplio el SLA."""
        self.fecha_cofirmacion = fecha or datetime.now(UTC)
        return self.evaluar_sla()


@dataclass
class Evento:
    """Agregado operativo que limita a 15 proveedores."""

    evento_id: str
    asignaciones: list[AsignacionProveedor] = field(default_factory=list)

    MAX_PROVEEDORES = 15

    def __post_init__(self) -> None:
        if len(self.asignaciones) > self.MAX_PROVEEDORES:
            raise ValueError("un evento no puede tener mas de 15 proveedores")

    @property
    def proveedores(self) -> list[AsignacionProveedor]:
        return self.asignaciones

    def asignar_proveedor(self, proveedor_id: str) -> AsignacionProveedor:
        if len(self.asignaciones) >= self.MAX_PROVEEDORES:
            raise ValueError("un evento no puede tener mas de 15 proveedores")
        asignacion = AsignacionProveedor(proveedor_id)
        self.asignaciones.append(asignacion)
        return asignacion


@dataclass
class CuentaDePagos:
    """Cuenta financiera que administra saldo, pagos y devoluciones."""

    saldo: float = 0.0

    def __post_init__(self) -> None:
        if self.saldo < 0:
            raise ValueError("el saldo no puede ser negativo")

    def registrar_pago(self, monto: float) -> float:
        self._validar_monto(monto)
        self.saldo += monto
        return self.saldo

    def devolver(self, monto: float) -> float:
        self._validar_monto(monto)
        if monto > self.saldo:
            raise ValueError("la devolucion no puede exceder el saldo")
        self.saldo -= monto
        return monto

    def calcular_devolucion(self, monto: float) -> float:
        return self.devolver(monto)

    @staticmethod
    def _validar_monto(monto: float) -> None:
        if monto <= 0:
            raise ValueError("el monto debe ser positivo")
