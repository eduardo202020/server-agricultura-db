from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.logic import process_query, process_miyawaki_question  # Importa las funciones lógicas

app = FastAPI()

# Modelo para el endpoint /question
class QuestionRequest(BaseModel):
    query: str
    type: str
    context: str

@app.post("/diagnosis")
async def get_diagnosis(query: str = Query(..., description="Consulta de diagnóstico")):
    try:
        # Llama a la lógica principal para procesar la consulta
        api_response = process_query(query)
        return JSONResponse(content=api_response)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.post("/question")
async def get_answer(request: QuestionRequest):
    try:
        # Procesar pregunta contextualizada sobre método Miyawaki Forest
        api_response = process_miyawaki_question(request.query, request.type, request.context)
        return JSONResponse(content=api_response)
            
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
