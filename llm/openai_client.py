from openai import OpenAI
from common.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_answer(prompt):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=100
    )

    return response.output_text if hasattr(response, "output_text") else str(response)