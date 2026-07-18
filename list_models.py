from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

for model in client.models.list():
    if "embed" in model.name.lower():
        print(model.name)