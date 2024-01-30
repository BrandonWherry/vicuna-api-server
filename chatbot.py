import textwrap
import requests
import json
from rich.console import Console

console = Console()
MAX_WIDTH = 80  # Set maximum characters per line

def chat_prompt(user_input: str) -> str:
    return (
        'You\'re an AI assistant, respond politely and honestly to the USER.\n'
        'Only write one AI response.\n'
        f'USER: {user_input}\n'
        'AI: '
    )

def get_completion_from_api(prompt, model='vicuna-13b-v1.5-16k'):
    url = 'http://127.0.0.1:8000/v1/completions'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        'model': model,
        'prompt': prompt,
        'max_tokens': 50,
        'temperature': 0.5,
    })

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        completion_text = response.json()['choices'][0]['text'].strip()
        return completion_text
    else:
        console.print(f"[red]Error:[/red] {response.status_code} - {response.text}")
        return None

def wrap_text(text, width=MAX_WIDTH, color=None):
    """Wrap text to the specified width."""
    wrapped_text = textwrap.fill(text, width)
    return f"[{color}]{wrapped_text}[/{color}]"

while True:
    console.print("[blue]USER: [/blue]", end="")
    user_input = input()
    
    if user_input.lower() == 'exit':
        break
    
    full_prompt = chat_prompt(user_input)
    
    completion_text = get_completion_from_api(full_prompt)
    
    if completion_text:
        ai_response = wrap_text(completion_text, color="green")
        console.print(f"[green]AI:[/green] {ai_response}")
    else:
        console.print("[red]Failed to get completion.[/red]")

console.print("[yellow]Goodbye![/yellow]")