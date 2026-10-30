from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./salon.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Master(Base):
    __tablename__ = "masters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)


class MasterResponse(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        from_attributes = True


Base.metadata.create_all(bind=engine)

db = SessionLocal()
if db.query(Master).count() == 0:
    db.add_all([
        Master(name="Анна", specialization="Парикмахер"),
        Master(name="Мария", specialization="Визажист"),
        Master(name="Ольга", specialization="Мастер маникюра"),
    ])
    db.commit()
db.close()


app = FastAPI()


@app.get("/masters", response_model=List[MasterResponse])
def get_masters(
    specialization: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Master)
    if specialization:
        query = query.filter(Master.specialization == specialization)
    return query.all()


@app.get("/masters/{master_id}", response_model=MasterResponse)
def get_master(master_id: int, db: Session = Depends(get_db)):
    master = db.query(Master).filter(Master.id == master_id).first()
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master