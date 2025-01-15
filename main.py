from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.logic import process_query  # Importa la función lógica

app = FastAPI()

@app.post("/diagnosis")
async def get_diagnosis(query: str):
    try:
        # Llama a la lógica principal para procesar la consulta
        api_response = process_query(query)
        return JSONResponse(content=api_response)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
