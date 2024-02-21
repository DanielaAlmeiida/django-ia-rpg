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
        user_authenticated = request.user.is_authenticated
        user_name = User.objects.get(pk=request.user.id)
        context = {
            'user_authenticated': user_authenticated,
            'user_name': user_name
        }
        return render(request, 'login.html', context)
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
        user_authenticated = request.user.is_authenticated
        context = {
            'user_authenticated': user_authenticated,
        }
        return render(request, 'login.html', context)
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
    return redirect("/login/")


def home(request):
    user_authenticated = request.user.is_authenticated

    if user_authenticated:
        user_name = User.objects.get(pk=request.user.id)
        context = {
            'user_authenticated': user_authenticated,
            'user_name': user_name
        }
        return render(request, 'home.html', context)

    context = {
        'user_authenticated': user_authenticated,
    }

    return render(request, 'home.html', context)


'''def header(request):
    user_authenticated = request.user.is_authenticated
    show = 'display: flex;' if user_authenticated else 'display: none;'
    context = {
        'show': show,
    }
    return render(request, 'header.html', context)'''


@login_required(login_url='/login/')
def generate_image(request):
    user_authenticated = request.user.is_authenticated
    user_name = User.objects.get(pk=request.user.id)
    context = {
        'user_authenticated': user_authenticated,
        'user_name': user_name
    }
    if request.method == 'POST':

        load_dotenv()
        secret_key = os.getenv("SEGMIND_API_KEY")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        url = "https://api.segmind.com/v1/sdxl1.0-samaritan-3d"



        category = request.POST.get('category')
        card_name = request.POST.get('card-name')
        card_description = request.POST.get('card-description')
        color = request.POST.get('color')
        type = request.POST.get('type')
        prompt = ''

        if category == 'Weapons':
            weapon_element = request.POST.get('weapon-element')
            prompt = (
                f"Give a brief description of a {color} {type} "
                f"named {card_name} imbued with an element of {weapon_element}."
                f"\nShort description entered by the user (optional): '{card_description}'")
        elif category == 'Potions':
            prompt = (
                f"Give a brief description of a {color} potion"
                f"named {card_name} imbued with an effect of {type}."
                f"\nShort description entered by the user (optional): '{card_description}'")
        elif category == 'Armors':
            armor_material = request.POST.get('armor-material')
            prompt = (
                f"Give a brief description of a {color} {type} armor"
                f"named {card_name} forged with an material of {armor_material}."
                f"\nShort description entered by the user (optional): '{card_description}'")


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
                               "person, Letters, names, words, Human being, doll, face, nose, eyes",
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
            weapon_suf = type[0] + type[1]
            display_none, display_block, display_flex, none = "display: none", "display: block", "display: flex", "none"
            user = User.objects.get(pk=request.user.id)

            cards = Card.objects.count()
            serial = cards + 1

            card = Card(
                user=user,
                name=card_name,
                rarity=rarity_card,
                image=byte_stream.read(),
                type=type,
                category=category,
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
                'user_authenticated': user_authenticated,
            }

            return render(request, 'index.html', context)

    return render(request, 'index.html', context)


def filter_cards_by_category(request):
    filter_value = request.GET.get('filter', 'all')

    if filter_value == 'weapon':
        return filter_cards_by_category(request, 'Weapons')
    elif filter_value == 'potion':
        return filter_cards_by_category(request, 'Potions')
    elif filter_value == 'armor':
        return filter_cards_by_category(request, 'Armors')
    elif filter_value != 'all':
        return filter_cards_by_category(request, filter_value)
    else:
        return filter_cards_by_category(request, 'all')


@login_required(login_url='/login/')
def inventory(request, category):
    user = User.objects.get(pk=request.user.id)
    if category == 'all':
        cards = Card.objects.filter(user=user).order_by('power').reverse()
    elif category in ['Armors', 'Weapons', 'Potions']:
        cards = Card.objects.filter(user=user, category=category).order_by('power').reverse()
    else:
        cards = Card.objects.filter(user=user, rarity=category).order_by('power').reverse()

    best_card = Card.objects.filter(user=user).order_by('power').reverse().first()
    status = Status.objects.filter(card=best_card)
    best_byte_stream = best_card.image
    best_image_base64 = base64.b64encode(best_byte_stream).decode('utf-8')
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

    user_authenticated = request.user.is_authenticated
    user_name = User.objects.get(pk=request.user.id)


    context = {
        'card_data_list': card_data,
        'best_card': best_card,
        'status': status,
        'best_image_base64': best_image_base64,
        'user_authenticated': user_authenticated,
        'user_name': user_name
    }

    return render(request, 'inventory.html', context)



def ranking(request, category):
    if category == 'all':
        cards = Card.objects.all().order_by('power').reverse()
    elif category in ['Armors', 'Weapons', 'Potions']:
        cards = Card.objects.filter(category=category).order_by('power').reverse()
    else:
        cards = Card.objects.filter(rarity=category).order_by('power').reverse()

    card_data = []
    for card in cards:
        status = Status.objects.filter(card=card)
        power_color, back_color = full_power_inventory(card.power)
        byte_stream = card.image
        image_base64 = base64.b64encode(byte_stream).decode('utf-8')

        card_data.append({
            'user': card.user.username,
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

    user_authenticated = request.user.is_authenticated
    user_name = ''
    if user_authenticated:
        user_name = User.objects.get(pk=request.user.id)

    context = {
        'ranking_list': card_data,
        'user_authenticated': user_authenticated,
        'user_name': user_name
    }

    return render(request, 'ranking.html', context)