import base64
import os
from dotenv import load_dotenv
from openai import OpenAI

from PIL import Image
from io import BytesIO

from django.shortcuts import render
import requests

def generateImage(request):
    if request.method == 'POST':
        load_dotenv()

        api_key = os.getenv("SEGMIND_API_KEY")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        url = "https://api.segmind.com/v1/sdxl1.0-samaritan-3d"

        weapon_type = request.POST.get('weapon-type')
        weapon_name = request.POST.get('weapon-name')
        weapon_color = request.POST.get('weapon-color')
        weapon_aura = request.POST.get('weapon-aura')
        weapon_description = request.POST.get('weapon-description')

        prompt = (f"Give a brief description of a {weapon_color} {weapon_type} named {weapon_name} imbued with an aura of {weapon_aura}."
                  f"Description: '{weapon_description}'")

        response_text = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt + "\nAfter creating the weapon description, summarize the description"},
            ]
        )

        final_prompt = response_text.choices[0].message.content

        print(final_prompt)

        data = {
          "prompt": final_prompt,
          "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, "
                             "deformed, ugly. young. long neck. (cross eyed:1.5). multiple characters, character, person",
          "samples": 1,
          "scheduler": "Euler a",
          "num_inference_steps": 25,
          "guidance_scale": 7.5,
          "seed": 4896513168,
          "img_width": 1024,
          "img_height": 1024,
          "base64": False
        }

        response = requests.post(url, json=data, headers={'x-api-key': api_key})
        print(response)

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.show()

            byte_stream = BytesIO()
            img.save(byte_stream, format='PNG')
            byte_stream.seek(0)

            imagem_base64 = base64.b64encode(byte_stream.getvalue()).decode('utf-8')

            context = {
                'imagem_base64': imagem_base64,
            }

            return render(request, 'generate_image.html', context)

    return render(request, 'generate_image.html')