"""Conexion a MySQL (Windows o contenedor) desde la app."""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - dotenv es opcional
    pass


def _wsl_host() -> str:
    """Detecta la IP del host de Windows (gateway por defecto de WSL)."""
    try:
        with open("/proc/net/route", encoding="utf-8") as fh:
            for line in fh.readlines()[1:]:
                fields = line.strip().split()
                if len(fields) >= 3 and fields[1] == "00000000":
                    gw = int(fields[2], 16)
                    return ".".join(str((gw >> (8 * i)) & 0xFF) for i in range(4))
    except Exception:
        pass
    return "127.0.0.1"


# Las credenciales se toman siempre del entorno (archivo .env en local).
HOST = os.getenv("MYSQL_HOST") or _wsl_host()
PORT = int(os.getenv("MYSQL_PORT", "3307"))
USER = os.getenv("MYSQL_USER", "appuser")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DATABASE = os.getenv("MYSQL_DATABASE", "appdb")

MYSQL_INFO = {"host": HOST, "port": PORT, "user": USER, "database": DATABASE}

_url = URL.create(
    "mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE,
    query={"charset": "utf8mb4"},
)

engine = create_engine(_url, pool_pre_ping=True, pool_recycle=1800)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
