# Gemini SDK Setup

Install:

```bash
pip install -U google-genai
```

Usage:

```python
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY"
)

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Hello"
)

print(response.text)
```