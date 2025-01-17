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
    Procesa una consulta del usuario y retorna una estructura JSON.
    """
    # Generar un embedding de la consulta
    query_embedding = embeddings.embed_query(query)

    # Buscar en Chroma con múltiples respuestas
    results = vectorstore.similarity_search_by_vector(query_embedding, k=2)

    # Procesar resultados y estructurar la respuesta
    response_data = []
    for result in results:
        # Preparar entrada para el modelo de chat
        messages = [
            {"role": "system", "content": "Eres un experto en plantas y jardinería."},
            {"role": "user", "content": f"""
            Diagnóstico: {result.metadata['name']}
            Resumido en una sola oración: {result.page_content}
            """}
        ]

        # Llamada al modelo de chat
        response = llm.invoke(messages)

        # Extraer respuesta procesada
        llm_response = response.content.strip()  # Obtener la respuesta del LLM

        # Validar si la respuesta está truncada
        if not llm_response.endswith(('.', '!', '?')):
            llm_response += "..."  # Indicar que está truncada

        # Crear estructura simplificada para la respuesta
        structured_response = {
            "diagnosis_name": result.metadata['name'],  # Nombre del diagnóstico
            "slug": getslug(result.metadata['name']),  # Slug del diagnóstico
            "short_description": llm_response,         # Respuesta breve del LLM
        }

        response_data.append(structured_response)

    # Estructurar la respuesta final
    return {
        "status": "success",
        "data": response_data
    }
