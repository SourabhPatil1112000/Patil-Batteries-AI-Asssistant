import os
import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, 'chatbot/index.html')

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv('SITE_URL'),
                "X-Title": os.getenv('SITE_NAME'),
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
            })
        )
        
        if response.status_code == 200:
            bot_response = response.json()['choices'][0]['message']['content']
            cleaned_response = bot_response.replace('**', '')
            return JsonResponse({'response': cleaned_response})
        else:
            return JsonResponse({'response': 'Sorry, I encountered an error. Please try again.'}, status=500)
    
    return render(request, 'chatbot/chat.html')