from app.services.rag_service import rag_service

response = rag_service.answer(
    "What is volatile matter?"
)

print("\nAnswer:\n")
print(response)