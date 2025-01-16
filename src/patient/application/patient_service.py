import csv
from io import StringIO
from typing import AsyncGenerator

from dependency_injector.wiring import inject
from ulid import ULID

from patient.domain.repository.patient_repo import IPatientRepository


class PatientService:
    @inject
    def __init__(self, patient_repo: IPatientRepository):
        self.patient_repo = patient_repo
        self.ulid = ULID()

    async def download_csv(self, limit: int | None) -> AsyncGenerator[str, None]:
        output = StringIO()
        writer = csv.writer(output)

        headers = ["pid", "patient_id", "patient_name", "patient_age", "birthdate", "result_status"]
        writer.writerow(headers)

        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        async for chunk in self.patient_repo.download_csv(limit):  # type: ignore
            print("chunk start")

            for patient in chunk:
                writer.writerow(
                    [
                        patient.pid,
                        patient.patient_id,
                        patient.patient_name,
                        patient.patient_age,
                        patient.birthdate.strftime("%Y-%m-%d") if patient.birthdate else "",
                        patient.result_status,
                    ]
                )
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)

        print("test")
