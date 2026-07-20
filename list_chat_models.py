from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

for model in client.models.list():
    # Only show models that support text generation
    if "generateContent" in getattr(model, "supported_actions", []):
        print(model.name)