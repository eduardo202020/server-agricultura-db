from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar embeddings y modelo de chat
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=80)  # Aumentado a 80 tokens


vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# funcion getslug para crear el slug en funcion del nombre del diagnostico
def getslug(name):
    slug = name.replace(" ", "-")
    return slug.lower()


def process_query(query: str):
    """
    Procesa una consulta del usuario sobre método Miyawaki y retorna una estructura JSON de diagnósticos.
    """
    # Crear un modelo para diagnósticos Miyawaki
    miyawaki_diagnosis_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=200)
    
    # Prompt especializado para generar diagnósticos sobre método Miyawaki
    messages = [
        {
            "role": "system", 
            "content": """Eres un especialista experto en el método Miyawaki Forest para la creación de bosques nativos.
            
            Cuando recibas una consulta, debes generar 2-3 "diagnósticos" o recomendaciones específicas sobre el método Miyawaki.
            Cada diagnóstico debe tener:
            - Un nombre/título específico relacionado con la consulta
            - Una descripción breve y práctica (máximo 100 caracteres)
            
            Enfócate en aspectos como:
            - Preparación del terreno y suelo
            - Selección de especies nativas
            - Técnicas de plantación de alta densidad
            - Cuidados y mantenimiento
            - Fases del desarrollo del bosque
            - Problemas comunes y soluciones
            
            Responde en formato: "DIAGNOSTICO1: descripción|DIAGNOSTICO2: descripción|DIAGNOSTICO3: descripción"
            Usa el separador "|" entre cada diagnóstico."""
        },
        {
            "role": "user", 
            "content": f"Consulta sobre método Miyawaki: {query}"
        }
    ]
    
    try:
        # Llamada a OpenAI
        response = miyawaki_diagnosis_llm.invoke(messages)
        llm_response = response.content.strip()
        
        # Procesar la respuesta para extraer los diagnósticos
        response_data = []
        
        # Dividir la respuesta por el separador "|"
        diagnosticos = llm_response.split("|")
        
        for i, diagnostico in enumerate(diagnosticos[:3]):  # Máximo 3 diagnósticos
            if ":" in diagnostico:
                # Separar nombre y descripción
                parts = diagnostico.split(":", 1)
                diagnosis_name = parts[0].strip()
                description = parts[1].strip()
            else:
                # Si no hay ":", usar el texto completo como descripción
                diagnosis_name = f"Recomendación Miyawaki {i+1}"
                description = diagnostico.strip()
            
            # Limpiar y limitar la descripción
            if len(description) > 100:
                description = description[:97] + "..."
            
            # Crear estructura de diagnóstico
            structured_response = {
                "diagnosis_name": diagnosis_name,
                "slug": getslug(diagnosis_name),
                "short_description": description
            }
            
            response_data.append(structured_response)
        
        # Si no se generaron diagnósticos válidos, crear uno por defecto
        if not response_data:
            response_data = [{
                "diagnosis_name": "Consulta sobre Método Miyawaki",
                "slug": "consulta-metodo-miyawaki",
                "short_description": "Consulta tu pregunta con un especialista en reforestación Miyawaki."
            }]
        
        return {
            "status": "success",
            "data": response_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al procesar la consulta Miyawaki: {str(e)}"
        }

def process_miyawaki_question(query: str, question_type: str, context: str):
    """
    Procesa preguntas específicas sobre el método Miyawaki Forest usando OpenAI.
    """
    # Crear un modelo con más tokens para respuestas completas
    miyawaki_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=300)
    
    # Definir el prompt especializado según el tipo de pregunta
    type_prompts = {
        "siembra": "siembra y plantación en bosques Miyawaki, incluyendo densidad de plantación, preparación del suelo y técnicas de siembra",
        "riego": "sistemas de riego y manejo hídrico en bosques Miyawaki, considerando las necesidades específicas de especies nativas",
        "fertilizacion": "fertilización y nutrición del suelo en el método Miyawaki, incluyendo compost y enmiendas orgánicas",
        "poda": "técnicas de poda y manejo silvícola en bosques Miyawaki para optimizar el crecimiento",
        "plagas": "control integrado de plagas y enfermedades en ecosistemas forestales Miyawaki",
        "cosecha": "cosecha sostenible y manejo de productos forestales en bosques Miyawaki",
        "trasplante": "técnicas de trasplante y establecimiento de plantas en el método Miyawaki",
        "compost": "preparación de compost y mejoramiento del suelo para bosques Miyawaki"
    }
    
    specialty_context = type_prompts.get(question_type, "aspectos generales del método Miyawaki")
    
    # Preparar el prompt para OpenAI
    messages = [
        {
            "role": "system", 
            "content": f"""Eres un especialista experto en el método Miyawaki Forest para la creación de bosques nativos. 
            Tu conocimiento abarca:
            - Técnicas de reforestación acelerada del Dr. Akira Miyawaki
            - Selección de especies nativas y pioneras
            - Preparación intensiva del suelo y biomasa
            - Plantación de alta densidad (3-5 plantas por m²)
            - Manejo ecológico y sostenible de ecosistemas forestales
            - Restauración de biodiversidad y servicios ecosistémicos
            
            Enfócate específicamente en: {specialty_context}
            
            Proporciona respuestas prácticas, científicamente fundamentadas y aplicables al método Miyawaki.
            Incluye consejos específicos y considera las particularidades de este método de reforestación."""
        },
        {
            "role": "user", 
            "content": query
        }
    ]
    
    try:
        # Llamada a OpenAI
        response = miyawaki_llm.invoke(messages)
        answer = response.content.strip()
        
        # Generar tips específicos basados en el tipo de pregunta
        tips_by_type = {
            "siembra": [
                "Planta entre 3-5 especies por metro cuadrado siguiendo el método Miyawaki",
                "Usa especies nativas de tu región para mayor supervivencia",
                "Mezcla especies pioneras con especies climácicas"
            ],
            "riego": [
                "Riega intensivamente los primeros 2-3 años hasta el establecimiento",
                "Reduce gradualmente el riego conforme el bosque madura",
                "Instala sistemas de riego por goteo para eficiencia hídrica"
            ],
            "fertilizacion": [
                "Prepara una capa de biomasa de 1 metro de altura",
                "Usa compost orgánico y evita fertilizantes químicos",
                "Incorpora micorrizas para mejorar la absorción de nutrientes"
            ],
            "poda": [
                "Evita la poda excesiva, permite el crecimiento natural",
                "Elimina solo ramas muertas o enfermas",
                "Respeta la competencia natural entre especies"
            ],
            "plagas": [
                "Fomenta la biodiversidad para control biológico natural",
                "Usa métodos orgánicos y evita pesticidas químicos",
                "Monitorea regularmente la salud del ecosistema"
            ],
            "cosecha": [
                "Permite al menos 10-15 años antes de cualquier cosecha",
                "Cosecha selectivamente respetando la estructura del bosque",
                "Mantén siempre la cobertura forestal principal"
            ],
            "trasplante": [
                "Transplanta durante la época de lluvias",
                "Usa plantas jóvenes de 60-80 cm de altura",
                "Asegura un buen establecimiento radicular antes del trasplante"
            ],
            "compost": [
                "Prepara compost con restos vegetales locales",
                "Mantén una relación C:N adecuada (25-30:1)",
                "Permite 6-12 meses de compostaje antes de usar"
            ]
        }
        
        tips = tips_by_type.get(question_type, [
            "Sigue los principios fundamentales del método Miyawaki",
            "Usa solo especies nativas de tu ecosistema local",
            "Mantén alta densidad de plantación para competencia natural"
        ])
        
        # Temas relacionados basados en el tipo de pregunta
        related_topics_map = {
            "siembra": ["fertilizacion", "compost", "trasplante"],
            "riego": ["siembra", "fertilizacion"],
            "fertilizacion": ["compost", "siembra", "riego"],
            "poda": ["plagas", "cosecha"],
            "plagas": ["poda", "fertilizacion"],
            "cosecha": ["poda", "trasplante"],
            "trasplante": ["siembra", "riego"],
            "compost": ["fertilizacion", "siembra"]
        }
        
        related_topics = related_topics_map.get(question_type, ["siembra", "riego"])
        
        return {
            "status": "success",
            "data": {
                "answer": answer,
                "tips": tips,
                "related_topics": related_topics,
                "timestamp": "2025-06-28T10:30:00Z"
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al procesar la pregunta sobre método Miyawaki: {str(e)}"
        }
