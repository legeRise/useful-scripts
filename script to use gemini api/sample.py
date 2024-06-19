import google.generativeai as genai
# from settings import API_KEY

PROMPT = """your prompt here"""


MODEL = 'gemini-pro'
print('** GenAI text: %r model & prompt %r\n' % (MODEL, PROMPT))

genai.configure(api_key="your-api-key-here")
model = genai.GenerativeModel(MODEL)

response = model.generate_content(PROMPT)
print(response.text)