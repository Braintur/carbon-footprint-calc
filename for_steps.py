from google import genai

API_KEY= "AIzaSyCkdc_A-FjHHbS5_EweBmn2OEjEJ4_GgnU"
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model='gemini-2.0-flash-lite', 
    contents='Tell me a story in 300 words.'
)
print(response.text)