# API de ejemplo — FastAPI + MySQL

Proyecto de desarrollo con **FastAPI** corriendo en **WSL Ubuntu 24.04** y **MySQL 8.4**.

## Estructura

```
projects/
├── main.py              # Endpoints FastAPI
├── db.py                # Engine/sesión SQLAlchemy (autodetecta host)
├── models.py            # Modelos (Base, Item)
├── alembic/             # Migraciones
├── tests/               # Tests (pytest + httpx; usan SQLite en memoria)
├── .github/workflows/   # CI (lint + tests + docker build)
├── Dockerfile
├── docker-compose.yml   # api + db (MySQL) + adminer
├── requirements.txt     # Dependencias de runtime
├── requirements-dev.txt # + pytest, ruff, httpx
├── start.sh             # Arranque rápido en local (venv)
└── .vscode/             # Debug F5, tasks y extensiones recomendadas
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Healthcheck |
| GET | `/db/ping` | Verifica conexión a la base de datos |
| GET | `/items` | Lista items |
| POST | `/items?nombre=...` | Crea un item |

Docs interactivas: http://localhost:8000/docs

## Opción 1 — Local con venv (usa el MySQL de Windows)

```bash
cd ~/projects
cp .env.example .env      # y pon tus credenciales
./start.sh                # http://localhost:8000
```

El host de MySQL se autodetecta desde el gateway de WSL.

## Opción 2 — Todo en contenedores (autocontenido)

```bash
cd ~/projects
docker compose up -d --build
# API:      http://localhost:8000
# Adminer:  http://localhost:8080
docker compose down
```

Puertos: API `8000`, MySQL `3308`, Adminer `8080`.
El contenedor `api` ejecuta `alembic upgrade head` al arrancar.

## Migraciones (Alembic)

```bash
./.venv/bin/alembic revision --autogenerate -m "descripcion"   # crear
./.venv/bin/alembic upgrade head                               # aplicar
./.venv/bin/alembic downgrade -1                               # revertir
./.venv/bin/alembic current
```

> Si apuntas Alembic a una base donde la tabla `items` ya existe (p. ej. el
> MySQL de Windows), marca el estado sin recrear nada:
> `./.venv/bin/alembic stamp head`

## Tests y lint

```bash
pip install -r requirements-dev.txt
ruff check .
pytest
```

Los tests usan SQLite en memoria, así que **no necesitan MySQL**.

## Credenciales

No se versionan. Cópialas a `.env` (ver `.env.example`). Los valores por
defecto que se crearon en este equipo están documentados en la sesión de
instalación; **cámbialos antes de usarlos en cualquier entorno compartido**.

| Entorno | Host | Puerto | Usuario |
|---|---|---|---|
| MySQL en Windows | `127.0.0.1` / `172.18.0.1` desde WSL | 3307 | `appuser`, `root` |
| MySQL en contenedor | `127.0.0.1` | 3308 | `appuser`, `root` |

## VS Code

Abre el proyecto desde la terminal de Ubuntu:

```bash
cd ~/projects && code .
```

Luego usa **F5 → "FastAPI (uvicorn --reload)"** para depurar.
Las extensiones recomendadas se instalan solas al abrir el workspace.
