from app.services.embedding_service import embedding_service

embedding = embedding_service.embed_query(
    "How long does Airtel fiber installation take?"
)

print(len(embedding))
print(embedding[:10])