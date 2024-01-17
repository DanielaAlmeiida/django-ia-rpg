import base64
import os
import random as rd

from dotenv import load_dotenv
from openai import OpenAI

from PIL import Image
from io import BytesIO

from django.shortcuts import render
import requests

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

        prompt = (f"Give a brief description of a {weapon_color} {weapon_type} named {weapon_name} imbued with an aura of {weapon_aura}."
                  f"Description: '{weapon_description}'")

        response_text = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": prompt + "\nAfter creating the weapon description, summarize the description"},
            ],
            model="gpt-3.5-turbo",
            max_tokens=45
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

        listOfRarity = ["Bronze", "Silver", "Gold", "Emerald", "Diamond", "Ruby", "Obsidian", "Opal"]

        def status_generator():

            status = 0
            lucky = rd.randint(1, 100)

            if lucky <= 40:
                status = rd.randint(10, 80)
            elif lucky <= 65:
                status = rd.randint(81, 130)
            elif lucky <= 80:
                status = rd.randint(131, 180)
            elif lucky <= 90:
                status = rd.randint(181, 220)
            elif lucky <= 95:
                status = rd.randint(221, 260)
            elif lucky <= 97:
                status = rd.randint(261, 300)
            elif lucky <= 99:
                status = rd.randint(301, 350)
            else:
                status = rd.randint(351, 500)

            return status

        def item_status():

            stat = status_generator()

            if stat <= 80:
                rarity = listOfRarity[0]
                stt = stat
            elif stat <= 130:
                rarity = listOfRarity[1]
                stt = stat
            elif stat <= 180:
                rarity = listOfRarity[2]
                stt = stat
            elif stat <= 220:
                rarity = listOfRarity[3]
                stt = stat
            elif stat <= 260:
                rarity = listOfRarity[4]
                stt = stat
            elif stat <= 300:
                rarity = listOfRarity[5]
                stt = stat
            elif stat <= 350:
                rarity = listOfRarity[6]
                stt = stat
            else:
                rarity = listOfRarity[7]
                stt = stat

            return rarity, stt

        def number_status():
            rarity_card, status = item_status()

            ore_img = ""
            rarity_status = []

            if rarity_card == "Bronze":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 1
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Silver":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 2
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Gold":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 3
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Emerald":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 4
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Diamond":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 5
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Ruby":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 6
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            elif rarity_card == "Obsidian":
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 6
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)
            else:
                ore_img = f"../static/css/img-ores/ore-{rarity_card}.png"
                i = 6
                for number in range(0, i):
                    rarity_carde, stats = item_status()
                    card_info = {'rarity': rarity_carde, 'status': stats}
                    rarity_status.append(card_info)

            return rarity_card, status, ore_img, rarity_status

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))

            byte_stream = BytesIO()
            img.save(byte_stream, format='PNG')
            byte_stream.seek(0)

            weapon_suf = weapon_type[0] + weapon_type[1]
            serial_number = "0001"
            type_weapon = f"[{weapon_type} - {weapon_suf}{serial_number}]"
            card_name = weapon_name
            hidden, display_none, display_block = "hidden", "display: none", "display: block"
            image_base64 = base64.b64encode(byte_stream.getvalue()).decode('utf-8')
            description = final_prompt
            rarity_card, status, ore_img, rarity_status = number_status()
            status_list = ['STR', 'INT', 'VIT', 'AGI', 'RES', 'LUC']
            type_status = rd.choice(status_list)

            context = {
                'type_status': type_status,
                'rarity_status': rarity_status,
                'status': status,
                'ore_img': ore_img,
                'rarity_card': rarity_card,
                'type_weapon': type_weapon,
                'card_name': card_name,
                'z': display_block,
                'y': display_none,
                'x': hidden,
                'description': description,
                'image_base64': image_base64,
            }

            return render(request, 'generate_image.html', context)

    return render(request, 'generate_image.html')

