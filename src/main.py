import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from containers import Container
from patient.interface.controllers.patient_controller import router as patient_routers
from sync import router as sync_routers
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
container = Container()  # type: ignore

app.include_router(user_routers)
app.include_router(patient_routers)
app.include_router(sync_routers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=4)
