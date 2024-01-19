from djangoProject.full_power import full_power

import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

from PIL import Image
from io import BytesIO

from django.shortcuts import render
import requests

from django.http import HttpResponse

def index(request):
    html = f'''
    <html>
        <body>
            <h1>Test Django deploy</h1>
        </body>
    </html>
    '''
    return HttpResponse(html)

def generateImage(request):
    if request.method == 'POST':

        load_dotenv()
        secret_key = os.getenv("SEGMIND_API_KEY")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        url = "https://api.segmind.com/v1/sdxl1.0-samaritan-3d"

        weapon_type = request.POST.get('weapon-type')
        weapon_name = request.POST.get('weapon-name')
        weapon_color = request.POST.get('weapon-color')
        weapon_aura = request.POST.get('weapon-aura')
        weapon_description = request.POST.get('weapon-description')

        prompt = (
            f"Give a brief description of a {weapon_color} {weapon_type} "
            f"named {weapon_name} imbued with an aura of {weapon_aura}."
            f"Description: '{weapon_description}'")

        response_text = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": prompt + "\nAfter creating the weapon description, "
                                     "Summarize the description in just 1 paragraph with a maximum of 50 tokens"},
            ],
            model="gpt-3.5-turbo",

        )

        final_prompt = response_text.choices[0].message.content

        print(final_prompt)

        data = {
            "prompt": final_prompt,
            "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, "
                               "deformed, ugly. young. long neck. (cross eyed:1.5). multiple characters, character, "
                               "person, Letters, names, words, Human being, doll",
            "samples": 1,
            "scheduler": "Euler a",
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
            "seed": 4896513168,
            "img_width": 1024,
            "img_height": 1024,
            "base64": False
        }

        response = requests.post(url, json=data, headers={'x-api-key': secret_key})

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))

            byte_stream = BytesIO()
            img.save(byte_stream, format='PNG')
            byte_stream.seek(0)

            power_color, final_status, color_back, rarity_card, status, rarity_status, value_status = full_power()
            weapon_suf = weapon_type[0] + weapon_type[1]
            serial_number_weapon = f"{weapon_suf}-000.001"
            type_weapon = f"[{weapon_type} - {status}]"
            card_name = weapon_name
            display_none, display_block, display_flex, none = "display: none", "display: block", "display: flex", "none"
            image_base64 = base64.b64encode(byte_stream.getvalue()).decode('utf-8')
            description = final_prompt

            context = {
                'color_back': color_back,
                'power_color': power_color,
                'final_status': final_status,
                'rarity_status': rarity_status,
                'status': status,
                'rarity_card': rarity_card,
                'type_weapon': type_weapon,
                'serial_number_weapon': serial_number_weapon,
                'card_name': card_name,
                'display_block': display_block,
                'display_none': display_none,
                'display_flex': display_flex,
                'none': none,
                'description': description,
                'image_base64': image_base64,
            }

            return render(request, 'generate_image.html', context)

    return render(request, 'generate_image.html')