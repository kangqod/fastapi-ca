from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Patient(Base):
    __tablename__ = "Patient"

    pid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    patient_name: Mapped[str] = mapped_column(String(36), nullable=False)
    patient_age: Mapped[int] = mapped_column(Integer, nullable=False)
    birthdate: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    result_status: Mapped[datetime] = mapped_column(String(12), nullable=False)
