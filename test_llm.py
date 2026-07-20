from app.services.llm_service import llm_service

response = llm_service.generate(
    """
    Tell me in one sentence what FastAPI is.
    """
)

print(response)