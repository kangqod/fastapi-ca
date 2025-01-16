from dependency_injector import containers, providers

from patient.application.patient_service import PatientService
from patient.infra.repository.patient_repo import PatientRepository
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["user.interface.controllers", "patient.interface.controllers"])

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    patient_repo = providers.Factory(PatientRepository)
    patient_service = providers.Factory(PatientService, patient_repo=patient_repo)
