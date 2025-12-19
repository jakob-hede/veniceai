#!/usr/bin/env python3

from pathlib import Path
import requests


class Veniceor:
    def __init__(self):
        super().__init__()
        self.project_dir = Path(__file__).parent
        for d in Path(__file__).parents:
            # print(f'Venicor d="{d}"')
            if d.name == 'veniceai':
                self.project_dir = d
                break
        print(f'project_dir: "{self.project_dir}"')
        self.secrets_dir = self.project_dir / 'secrets'
        self.url = 'https://api.venice.ai/api/v1/chat/completions'
        self.default_key_name = 'inference01'
        self.default_api_key = self.get_api_key(self.default_key_name)
        self.default_model = 'llama-3.3-70b'
        self.default_temperature = 0.7
        self.default_max_tokens = 150
        self.default_system_prompt = 'You are a helpful assistant.'

    def get_api_key(self, key_name: str) -> str:
        api_file = self.secrets_dir / f'{key_name}.apikey.txt'
        if not api_file.exists():
            raise ValueError(f'API key file not found: "{api_file}"')
        api_key = api_file.read_text().strip()
        if not api_key:
            raise ValueError('API key not set.')
        return api_key

    def test_01(self):
        """
        The definitive, working example based on Venice.ai API docs:
        https://docs.venice.ai/api-reference/endpoint/chat/completions
        """
        key_name = 'inference01'
        api_key = self.get_api_key(key_name)
        # if not api_key:
        #     raise ValueError('API key not set.')

        # 1. THE CORRECT ENDPOINT (per docs: /api/v1/chat/completions)
        url = 'https://api.venice.ai/api/v1/chat/completions'

        # 2. HEADERS
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # 3. PAYLOAD: Chat completion format with 'messages'
        payload = {
            'model': 'llama-3.3-70b',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'Explain the concept of a REST API in simple terms.'}
            ],
            'temperature': 0.7,
            'max_tokens': 150
        }

        print(f'Attempting request to: {url}')
        print(f'Payload: {payload}')
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f'Status code: {response.status_code}')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
            if hasattr(e, 'response') and e.response is not None:
                print(f'Error Status Code: {e.response.status_code}')
                print(f'Error Response Body: {e.response.text}')
            return

        # 4. RESPONSE PARSING
        data = response.json()
        print(f'Response: {data}')
        generated_text = data['choices'][0]['message']['content'].strip()
        print('--- Generated Text ---')
        print(generated_text)
        print('---------------------')

    def prompt(self, user_prompt: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.default_api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.default_model,
            'messages': [
                {'role': 'system', 'content': self.default_system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': self.default_temperature,
            'max_tokens': self.default_max_tokens
        }
        response = requests.post(self.url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        generated_text = data['choices'][0]['message']['content'].strip()
        return generated_text

    def show_transition(self, user_prompt: str):
        print('Veniceor transition method called.')
        generated_text = self.prompt(user_prompt)
        print('--- Prompt ---')
        print(user_prompt)
        print('--- Generated Text ---')
        print(generated_text)
        print('---------------------')


class DissidentExpert(Veniceor):
    def __init__(self):
        super().__init__()
        # print('DissidentExpert initialized.')
        self.default_model = 'venice-uncensored'
        self.default_temperature = 0.2
        self.default_max_tokens = 1024
        self.default_system_prompt = 'You are a highly knowledgeable and critical thinker who provides in-depth analysis and alternative perspectives on various topics. Your responses should challenge conventional wisdom and encourage readers to think independently.'

# def main():
#     print(f'main {__file__}')
#     ox = Veniceor()
#     ox.test_01()
#
#
# if __name__ == '__main__':
#     main()
