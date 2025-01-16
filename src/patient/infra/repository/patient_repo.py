from typing import AsyncGenerator, Sequence

from sqlalchemy.future import select

from database import AsyncSessionLocal
from patient.domain.repository.patient_repo import IPatientRepository
from patient.infra.schema.patient import Patient


class PatientRepository(IPatientRepository):
    async def download_csv(self, limit: int | None) -> AsyncGenerator[Sequence[Patient], None]:
        chunk_size = 1000
        offset = 0

        while True:
            current_chunk = chunk_size if limit is None else min(chunk_size, limit - offset)

            # 쿼리 작성 (limit과 offset을 이용하여 데이터 청크 처리)
            query = select(Patient).limit(current_chunk).offset(offset)
            async with AsyncSessionLocal() as db:
                result = await db.execute(query)
                chunk = result.scalars().all()

                # 데이터가 없으면 종료
                if not chunk:
                    break

                # 데이터를 청크 단위로 반환
                yield chunk

                # offset 업데이트
                offset += len(chunk)
