import enum
import random
from datetime import datetime, timedelta
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from containers import Container
from database import SessionLocal
from patient.application.patient_service import PatientService
from patient.infra.schema.patient import Patient

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/download-csv", status_code=200)
@inject
async def download_csv(limit: Optional[int] = None, patient_service: PatientService = Depends(Provide[Container.patient_service])):
    return StreamingResponse(
        patient_service.download_csv(limit),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=patients.csv", "Content-Type": "text/csv; charset=utf-8"},
    )


class ResultStatusEnum(str, enum.Enum):
    abnormal = "abnormal"
    no_findings = "no_findings"


@router.post("", status_code=200)
@inject
async def create_patients(patient_service: PatientService = Depends(Provide[Container.patient_service])):
    print("Inserting sample patient data...")

    with SessionLocal() as session:
        batch_size = 10000  # 한 번에 삽입할 데이터 배치 크기
        total_records = 2000000  # 총 삽입할 레코드 수
        batches = total_records // batch_size

        for batch in range(batches):
            print("ulid : ", patient_service.ulid)
            patients = generate_sample_patients(patient_service.ulid, batch_size)
            session.add_all(patients)  # 데이터를 한 번에 추가
            session.commit()  # 커밋
            print(f"Batch {batch + 1}/{batches} inserted")

        session.close()

    print("Data insertion complete.")

    return {"results": "Good"}


# 샘플 데이터를 삽입하는 예시
def generate_sample_patients(ulid, batch_size=10000):
    """배치 사이즈로 데이터를 생성하고 반환"""
    patients = []
    for _ in range(batch_size):
        pid = ulid.generate()
        patient_name = f"Patient-{random.randint(1, 1000000)}"
        patient_age = random.randint(18, 90)
        birthdate = datetime.today() - timedelta(days=random.randint(18 * 365, 90 * 365))
        result_status = random.choice([e.value for e in ResultStatusEnum])
        patients.append(Patient(pid=pid, patient_id=pid, patient_name=patient_name, patient_age=patient_age, birthdate=birthdate, result_status=result_status))
    return patients
