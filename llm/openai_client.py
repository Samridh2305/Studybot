from openai import OpenAI
from common.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_answer(prompt):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=100
    )
    if hasattr(response, "output_text"):
        return response.output_text
    else:
        return str(response)