from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    api_key='ollama',
    base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
)

PROMPTS = {
    'short': '''You are a document analyst. Given document text, return JSON with:
  summary (1 sentence), key_points (up to 3, as strings), entities (up to 3, as {name, type}),
  document_type (invoice|contract|report|other).
  Return ONLY valid JSON, no extra text.''',

    'medium': '''You are a document analyst. Given document text, return JSON with:
  summary (2-3 sentences), key_points (up to 5, as strings), entities (array of {name, type}),
  document_type (invoice|contract|report|other).
  Return ONLY valid JSON, no extra text.''',

    'long': '''You are a document analyst. Given document text, return JSON with:
  summary (4-6 sentences with detailed analysis), key_points (up to 10, as strings, be thorough),
  entities (all entities found, as {name, type}),
  document_type (invoice|contract|report|other).
  Return ONLY valid JSON, no extra text.'''
}

async def analyze(text: str, detail: str = 'medium') -> dict:
    system_prompt = PROMPTS.get(detail, PROMPTS['medium'])
    resp = await client.chat.completions.create(
        model='llama3.2:1b',
        response_format={'type': 'json_object'},
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': text}
        ]
    )
    return resp.choices[0].message.content
