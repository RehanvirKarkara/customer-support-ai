from app.services.prompt_builder import prompt_builder

chunks = [
    {
        "document": "Airtel Fiber offers high-speed broadband services."
    },
    {
        "document": "Users can upgrade plans through the Airtel Thanks app."
    },
]

prompt = prompt_builder.build_prompt(
    query="How can I upgrade my Airtel Fiber plan?",
    retrieved_chunks=chunks,
)

print(prompt)