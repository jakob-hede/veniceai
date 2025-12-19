#!/usr/bin/env python3
"""Query Venice.ai API for available models."""

from pathlib import Path
import requests

def main():
    project_dir = Path(__file__).parent.parent
    secrets_dir = project_dir / 'secrets'
    api_file = secrets_dir / 'inference01.apikey.txt'
    api_key = api_file.read_text().strip()
    
    headers = {'Authorization': f'Bearer {api_key}'}
    
    try:
        response = requests.get('https://api.venice.ai/api/v1/models', headers=headers, timeout=30)
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print('\nAvailable models:')
            for model in data.get('data', []):
                model_id = model.get('id', 'unknown')
                print(f'  - {model_id}')
        else:
            print(f'Response: {response.text}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

