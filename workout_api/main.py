from fastapi import FastAPI
from workout_api.routers import api_router
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import add_pagination


app = FastAPI(title='WorkoutApi')
app.include_router(api_router)

app = FastAPI(title='WorkoutApi')
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_detail = str(exc.orig)
    cpf_match = [part for part in error_detail.split() if 'cpf' in part] 
    
    msg = f"Já existe um atleta cadastrado com o CPF informado."
    
    try:
        cpf_value = str(exc.params[0]) if exc.params else "desconhecido"
        msg = f"Já existe um atleta cadastrado com o cpf: {cpf_value}"
    except (IndexError, TypeError):
        pass

    return JSONResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        content={"detail": msg},
    )

add_pagination(app)
