from openai import OpenAI
import tiktoken
from apps.func import security_scans

obsufication_check=False

class ChatGPTClient:
    def __init__(self, file_path, model="gpt-3.5-turbo", max_tokens=4096):
        self.model = model
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model)
        self.encoding = tiktoken.encoding_for_model(model)
        self.file_path = file_path

    def get_response(self, prompt, response_max_tokens=2048, temperature=0.4):

        prompt_tokens = self.encoding.encode(prompt)
        prompt_token_length = len(prompt_tokens)
        available_prompt_tokens = self.max_tokens - response_max_tokens

        if prompt_token_length > available_prompt_tokens:
            prompt_chunks = self.split_prompt(prompt_tokens, available_prompt_tokens)
            responses = []
            for chunk in prompt_chunks:
                chunk_text = self.encoding.decode(chunk)
                response = self._send_request(chunk_text, response_max_tokens, temperature)
                responses.append(response)
            return "\n\n".join(responses)
        else:
            return self._send_request(prompt, response_max_tokens, temperature)

    def split_prompt(self, tokens, max_tokens_per_chunk):
        return [tokens[i:i + max_tokens_per_chunk] for i in range(0, len(tokens), max_tokens_per_chunk)]

    def _send_request(self, prompt, response_max_tokens, temperature):
        client = OpenAI(
            api_key="REDACTED"
        )

        try:
            response = client.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": "You can answer only RFC8259 compliant JSON response. You are an assistant that generates JSON. You always return just the JSON with no additional description or context."},
                {"role": "user", "content": prompt}
                ],
            max_tokens=response_max_tokens,
            temperature=temperature)
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error: {str(e)}"