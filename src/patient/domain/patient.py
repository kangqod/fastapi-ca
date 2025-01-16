from dataclasses import dataclass
from datetime import datetime


@dataclass
class Patient:
    pid: str
    patient_id: str
    patient_name: str
    patient_age: int
    birthdate: datetime
    result_status: str
