#!/usr/bin/env python3

import os
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

    def get_api_key(self, key_name: str) -> str:
        api_file = self.secrets_dir / f'{key_name}.apikey.txt'
        if not api_file.exists():
            raise ValueError(f'API key file not found: "{api_file}"')
        api_key = api_file.read_text().strip()
        return api_key

    def test_01(self):
        """
        The definitive, working example based on Venice.ai API docs:
        https://docs.venice.ai/api-reference/endpoint/chat/completions
        """
        key_name = 'inference01'
        api_key = self.get_api_key(key_name)
        if not api_key:
            raise ValueError("API key not set.")

        # 1. THE CORRECT ENDPOINT (per docs: /api/v1/chat/completions)
        url = "https://api.venice.ai/api/v1/chat/completions"

        # 2. HEADERS
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 3. PAYLOAD: Chat completion format with 'messages'
        payload = {
            "model": "llama-3.3-70b",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain the concept of a REST API in simple terms."}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        print(f"Attempting request to: {url}")
        print(f"Payload: {payload}")
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"Status code: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error Status Code: {e.response.status_code}")
                print(f"Error Response Body: {e.response.text}")
            return

        # 4. RESPONSE PARSING
        data = response.json()
        print(f"Response: {data}")
        generated_text = data['choices'][0]['message']['content'].strip()
        print("--- Generated Text ---")
        print(generated_text)
        print("---------------------")


def main():
    print(f'main {__file__}')
    ox = Veniceor()
    ox.test_01()


if __name__ == '__main__':
    main()

#################

# def working_chat_completion(self):
#     """
#     A working example for chat completion models like Llama 3.3.
#     """
#     key_name = 'inference01'
#     api_key = self.get_api_key(key_name)
#     if not api_key:
#         raise ValueError("VENICE_API_KEY environment variable not set.")
#
#     # 1. CORRECT ENDPOINT: Use the plural /completions
#     url = "https://api.venice.ch/api/v1/completions"
#
#     # 2. HEADERS are correct
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#
#     # 3. CORRECT PAYLOAD: Use the 'messages' format for chat models
#     payload = {
#         "model": "llama-3.3-70b",
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Explain the concept of a REST API in simple terms."}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 150
#     }
#
#     # Make the POST request
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         # You might want to check e.response here for more details
#         if e.response is not None:
#             print(f"Error Status Code: {e.response.status_code}")
#             print(f"Error Response Body: {e.response.text}")
#         return
#
#     # 4. CORRECT RESPONSE PARSING: The structure is slightly different
#     data = response.json()
#     # The content is nested deeper: choices -> message -> content
#     generated_text = data['choices'][0]['message']['content'].strip()
#     print(generated_text)
#
# def test01(self):
#     key_name = 'inference01'
#     api_key = self.get_api_key(key_name)
#     print(f'api_key: "{api_key}"')
#
# def get_api_key(self, key_name: str) -> str:
#     api_file = self.secrets_dir / f'{key_name}.apikey.txt'
#     if not api_file.exists():
#         raise ValueError(f'API key file not found: "{api_file}"')
#     api_key = api_file.read_text().strip()
#     return api_key
#
# def test02(self):
#
#     # It's best practice to load the API key from an environment variable
#     # api_key = os.getenv("VENICE_API_KEY")
#     key_name = 'inference01'
#     api_key = self.get_api_key(key_name)
#
#     if not api_key:
#         raise ValueError("VENICE_API_KEY environment variable not set.")
#
#     # The API endpoint for text completions
#     url = "https://api.venice.ai/api/v1/completion"
#
#     # The headers, including your API key for authentication
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#
#     # The payload containing your request parameters
#     # You can specify the model, prompt, and other options
#     payload = {
#         "model": "llama-3.3-70b",  # A good default model to start with
#         "prompt": "Explain the concept of a REST API in simple terms.",
#         "temperature": 0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
#         "max_tokens": 150  # Maximum number of tokens to generate in the response
#     }
#
#     # Make the POST request
#     response = requests.post(url, headers=headers, json=payload)
#
#     # Handle the response
#     if response.status_code == 200:
#         data = response.json()
#         # The generated text is in the 'choices' list
#         generated_text = data['choices'][0]['text'].strip()
#         print(generated_text)
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)
#
# def test03(self):
#     key_name = 'inference01'
#     api_key = self.get_api_key(key_name)
#
#     if not api_key:
#         raise ValueError("VENICE_API_KEY environment variable not set.")
#
#     # Candidate endpoints and simple variants (with/without trailing slash)
#     base_candidates = [
#         "https://api.venice.ai/api/v1/completion",
#         "https://api.venice.ai/api/v1/completions",
#         "https://api.venice.ai/v1/completions",
#         "https://api.venice.ai/v1/completion",
#     ]
#     candidate_urls = []
#     for u in base_candidates:
#         candidate_urls.append(u.rstrip("/"))
#         candidate_urls.append(u.rstrip("/") + "/")
#     # remove duplicates while preserving order
#     seen = set()
#     candidate_urls = [x for x in candidate_urls if not (x in seen or seen.add(x))]
#
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#
#     # Try several common payload shapes used by inference APIs
#     payload_variants = [
#         {"model": "llama-3.3-70b", "prompt": "Explain the concept of a REST API in simple terms.",
#          "temperature": 0.7, "max_tokens": 150},
#         {"model": "llama-3.3-70b", "input": "Explain the concept of a REST API in simple terms.",
#          "temperature": 0.7},
#         {"model": "llama-3.3-70b",
#          "messages": [{"role": "user", "content": "Explain the concept of a REST API in simple terms."}],
#          "temperature": 0.7},
#     ]
#
#     def extract_text_from_body(body):
#         if isinstance(body, dict):
#             # OpenAI-like
#             choices = body.get("choices") or body.get("results")
#             if choices and isinstance(choices, list) and len(choices) > 0:
#                 first = choices[0]
#                 # try common fields
#                 for key in ("text", "message", "content", "output"):
#                     if isinstance(first, dict) and first.get(key):
#                         val = first.get(key)
#                         if isinstance(val, str) and val.strip():
#                             return val.strip()
#                         if isinstance(val, list) and len(val) > 0 and isinstance(val[0], str):
#                             return val[0].strip()
#                 # sometimes choices[0] contains nested dicts
#                 if isinstance(first, dict):
#                     for v in first.values():
#                         if isinstance(v, str) and v.strip():
#                             return v.strip()
#             # some APIs return outputs or data arrays
#             outputs = body.get("output") or body.get("outputs") or body.get("data")
#             if isinstance(outputs, list) and len(outputs) > 0:
#                 item = outputs[0]
#                 if isinstance(item, dict):
#                     for key in ("text", "content", "message"):
#                         if item.get(key):
#                             val = item.get(key)
#                             if isinstance(val, str):
#                                 return val.strip()
#             # fallback: any top-level string field
#             for k, v in body.items():
#                 if isinstance(v, str) and v.strip():
#                     return v.strip()
#         return None
#
#     for url in candidate_urls:
#         print(f"Trying URL: {url}")
#         print(f"Headers: {headers}")
#         try:
#             # Probe supported methods / quick server info
#             try:
#                 opts = requests.options(url, headers=headers, timeout=5)
#                 print(f"OPTIONS {url} -> {opts.status_code}, headers: {dict(opts.headers)}")
#                 try:
#                     print("OPTIONS body:", opts.json())
#                 except Exception:
#                     if opts.text:
#                         print("OPTIONS text:", opts.text[:1000])
#             except requests.RequestException as e:
#                 print(f"OPTIONS failed: {e}")
#
#             for payload in payload_variants:
#                 print(f"Payload: {payload}")
#                 try:
#                     response = requests.post(url, headers=headers, json=payload, timeout=10)
#                 except requests.RequestException as e:
#                     print(f"Request failed: {e}")
#                     continue
#
#                 print(f"Status code: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
#                 body = None
#                 try:
#                     body = response.json()
#                     print("Response JSON:", body)
#                 except ValueError:
#                     body = response.text
#                     print("Response text:", body[:2000])
#
#                 if response.status_code in (200, 201):
#                     text = extract_text_from_body(body)
#                     if text:
#                         print("Generated text:\n", text)
#                         return
#                     else:
#                         print("200 OK but unexpected response shape. Full body printed above.")
#                         return
#                 elif response.status_code == 404:
#                     print("404 Not Found - endpoint likely incorrect. Trying next candidate.")
#                     break  # try next url
#                 elif response.status_code in (401, 403):
#                     print(f"Auth error {response.status_code}. Check API key/permissions.")
#                     return
#                 else:
#                     print(f"Error: {response.status_code}")
#                     # already printed body
#                     # try next payload for same url
#                     continue
#         except Exception as e:
#             print(f"Unexpected error while probing {url}: {e}")
#             continue
#
#     print(
#         "All candidate endpoints and payload shapes tried. Verify the correct endpoint and request format in the Venice API docs.")
