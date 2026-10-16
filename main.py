from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from db import MYSQL_INFO, SessionLocal, engine
from models import Item

app = FastAPI(title="API de ejemplo", version="0.3.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"mensaje": "Hola desde FastAPI en Ubuntu 24.04"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db/ping")
def db_ping():
    """Comprueba la conexion con la base de datos."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            dialect = engine.dialect.name
            version = database = None
            if dialect == "mysql":
                version = conn.execute(text("SELECT VERSION()")).scalar()
                database = conn.execute(text("SELECT DATABASE()")).scalar()
        return {
            "ok": True,
            "dialect": dialect,
            "mysql": version,
            "database": database,
            **MYSQL_INFO,
        }
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Error de conexion: {exc}") from exc


@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    try:
        items = db.scalars(select(Item).order_by(Item.id)).all()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Error de conexion: {exc}") from exc
    return {"total": len(items), "items": [i.to_dict() for i in items]}


@app.post("/items", status_code=201)
def create_item(nombre: str, db: Session = Depends(get_db)):
    item = Item(nombre=nombre)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item.to_dict()
