from app.services.retriever_service import retriever_service

results = retriever_service.retrieve(
    "What is Airtel Fiber?"
)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 50)
    print(result["document"])
    print(result["metadata"])
    print(result["score"])