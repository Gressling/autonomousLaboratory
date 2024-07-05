import openai

class OpenAIHandler:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()