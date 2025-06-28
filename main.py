from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.logic import process_query  # Importa la función lógica

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
        # Procesar pregunta contextualizada del calendario
        # Por ahora usamos la misma lógica, pero puedes crear una función específica
        api_response = process_query(request.query)
        
        # Convertir la respuesta del diagnóstico a formato de pregunta simple
        if api_response.get("status") == "success" and api_response.get("data"):
            # Tomar la primera respuesta y convertirla a formato simple
            first_result = api_response["data"][0]
            answer = f"{first_result['diagnosis_name']}: {first_result['short_description']}"
            
            return JSONResponse(content={
                "status": "success",
                "data": {
                    "answer": answer,
                    "tips": ["Consulta con un especialista si los síntomas persisten", "Mantén un monitoreo regular de tus plantas"],
                    "related_topics": [request.type],
                    "timestamp": "2025-06-28T10:30:00Z"
                }
            })
        else:
            return JSONResponse(
                content={"status": "error", "message": "No se pudo procesar la pregunta."},
                status_code=500
            )
            
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
