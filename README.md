# EventosNova-U5-Pruebas

Unidad 5 (Integracion, Pruebas y Calidad) de Componentes de Logica de Negocios, FIME-UANL. Equipo 16.
Reglas de negocio tomadas del PIA: https://github.com/FllyTMCruz/EventosNova

## Estructura hibrida
- `src/domain.py, application.py, repository.py, security.py`: proyecto base del laboratorio (Pasos 1-8, E1-E8). Dominio de pedidos.
- `src/eventos_nova/`: dominio del PIA (Paso 9, E9).
- `tests/`: pruebas del laboratorio; `tests/test_eventos_nova/`: pruebas del PIA.
- `docs/unidad5/`: evidencias, matriz CSV, bitacora de IA y reflexion.
- `.github/workflows/ci.yml`: pipeline (Ruff, pytest con cobertura >= 80%, compileall).

## Instalacion (Windows PowerShell)
```
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Comandos
```
python -m pytest -v
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
```
El reporte HTML queda en `htmlcov/index.html`.

## Flujo de trabajo del equipo
Cada integrante trabaja en su rama (`int1-...`, `int2-pruebas`, `int3-...`) y se integra a `main` con pull request.

## Notas del proyecto base
La regla de cancelacion impide cancelar pedidos enviados incluso para administrador. El pipeline hace verificacion de build (compileall), no despliegue.