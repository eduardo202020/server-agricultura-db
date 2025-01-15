# Diagnóstico de Plantas con FastAPI, LangChain y OpenAI

Este proyecto utiliza **FastAPI**, **LangChain**, **OpenAI** y **Chroma** para crear una API que permite diagnosticar problemas en plantas basándose en descripciones proporcionadas por los usuarios. Además, devuelve sugerencias de tratamiento y referencias útiles para abordar los problemas identificados.

---

## 🚀 Características

- Procesa descripciones de problemas en plantas y devuelve:
  - Diagnóstico breve.
  - Sugerencias de tratamiento resumidas.
  - Referencias útiles basadas en un libro especializado.
- Almacenamiento y búsqueda vectorial de datos con **Chroma**.
- Uso de **OpenAI** para generar respuestas concisas y contextuales.
- Control de límite de uso para proteger la API.
- Preparado para despliegue en plataformas en la nube como **Railway** o **AWS**.

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework para la creación de APIs rápidas y robustas.
- **LangChain**: Manejo de cadenas LLM y búsquedas vectoriales.
- **OpenAI API**: Generación de texto contextual basado en GPT-3.5 Turbo.
- **Chroma**: Base de datos vectorial para búsquedas eficientes.
- **Redis**: Almacenamiento para control de límite de uso.
- **Python**: Lenguaje de programación principal.

---

## 📦 Instalación

### **1. Clona el Repositorio**
```bash
git clone https://github.com/tu_usuario/diagnostico-plantas.git
cd diagnostico-plantas
```
