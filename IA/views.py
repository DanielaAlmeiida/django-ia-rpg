import os
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.http import HttpResponse

from IA.full_power import full_power
import base64

from dotenv import load_dotenv
from openai import OpenAI

from PIL import Image
from io import BytesIO

from django.shortcuts import render
import requests

from IA.models import Card, Status
from IA.full_power_inventory import full_power_inventory


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/generate/')
        else:
            return HttpResponse('Senha e/ou user incorretos')


def logout(request):
    auth.logout(request)
    return redirect("/generate/")


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')


@login_required(login_url='/login/')
def generate_image(request):
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
            f"\nShort description entered by the user (optional): '{weapon_description}'")

        response_text = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": prompt + "\n Make the description no longer than 3 lines"},
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

            image_base64 = base64.b64encode(byte_stream.getvalue()).decode('utf-8')
            power_color, final_status, color_back, rarity_card, status, rarity_status = full_power()
            weapon_suf = weapon_type[0] + weapon_type[1]
            display_none, display_block, display_flex, none = "display: none", "display: block", "display: flex", "none"
            user = User.objects.get(pk=request.user.id)

            cards = Card.objects.count()
            serial = cards + 1

            card = Card(
                user=user,
                name=weapon_name,
                rarity=rarity_card,
                image=byte_stream.read(),
                type=weapon_type,
                status_card=status,
                power=final_status,
                description=final_prompt
            )

            serial_number_weapon = f"{weapon_suf}-{str(serial).zfill(6)}"
            card.serial = serial_number_weapon
            type_weapon = f"[{card.type} - {card.status_card}]"

            card.save()

            for data in rarity_status:
                status_card = Status(
                    card=card,
                    rarity=data.get('rarity'),
                    attribute=data.get('type'),
                    stats=data.get('status')
                )

                status_card.save()

            context = {
                'card': card,
                'color_back': color_back,
                'power_color': power_color,
                'rarity_status': rarity_status,
                'type_weapon': type_weapon,
                'display_block': display_block,
                'display_none': display_none,
                'display_flex': display_flex,
                'none': none,
                'image_base64': image_base64,
            }

            return render(request, 'index.html', context)

    return render(request, 'index.html')


def filter_cards_by_category(request):
    filter_value = request.GET.get('filter', 'all')

    if filter_value == 'weapon':
        return filter_cards_by_category(request, 'Weapons')
    elif filter_value == 'potion':
        return filter_cards_by_category(request, 'Potions')
    elif filter_value == 'armor':
        return filter_cards_by_category(request, 'Armors')
    else:
        return filter_cards_by_category(request, 'all')


def inventory(request, category):
    user = User.objects.get(pk=request.user.id)
    if category == 'all':
        cards = Card.objects.filter(user=user).order_by('power').reverse()
    else:
        cards = Card.objects.filter(user=user, category=category)

    card_data = []
    for card in cards:
        power_color, back_color = full_power_inventory(card.power)
        byte_stream = card.image
        image_base64 = base64.b64encode(byte_stream).decode('utf-8')
        card_data.append({
            'name': card.name,
            'rarity': card.rarity,
            'image_base64': image_base64,
            'power_color': power_color,
            'back_color': back_color,
            'power': card.power,
        })

    context = {
        'card_data_list': card_data,
    }

    return render(request, 'inventory.html', context)


def ranking(request, category):
    user = User.objects.get(pk=request.user.id)
    if category == 'all':
        cards = Card.objects.filter(user=user).order_by('power').reverse()
    else:
        cards = Card.objects.filter(user=user, category=category).order_by('power').reverse()

    card_data = []
    for card in cards:
        status = Status.objects.filter(card=card)
        power_color, back_color = full_power_inventory(card.power)
        byte_stream = card.image
        image_base64 = base64.b64encode(byte_stream).decode('utf-8')

        card_data.append({
            'name': card.name,
            'rarity': card.rarity,
            'image_base64': image_base64,
            'type': card.type,
            'status_card': card.status_card,
            'power_color': power_color,
            'back_color': back_color,
            'power': card.power,
            'serial': card.serial,
            'status': status,
        })

    context = {
        'ranking_list': card_data,
    }

    return render(request, 'ranking.html', context)