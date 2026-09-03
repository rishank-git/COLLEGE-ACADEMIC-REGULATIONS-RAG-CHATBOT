from google import genai
from src.config import GEMINI_API_KEY

class GeminiLLM:
    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options={"timeout": 120000}
        )

    def ask(self, context, question):
        prompt = f"""
You are an Academic Regulation Assistant.

Answer ONLY from the academic regulations provided in the context.

Rules:
- Do not use outside knowledge.
- If the answer is not available in the context, reply exactly:
"I couldn't find this information in the academic regulations."
- Give a clear and concise answer.
- Mention the relevant section number when available.

Context:
{context}

Question:
{question}
"""
        # Use generate_content_stream instead of generate_content
        response = self.client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=prompt
        )

        # Yield each chunk of text as it arrives from the API
        for chunk in response:
            if chunk.text:
                yield chunk.text

