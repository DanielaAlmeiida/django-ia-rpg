import base64

from PIL import Image
from io import BytesIO

from django.shortcuts import render
import requests


def generateImage(request):
    if request.method == 'POST':
        api_key = "SG_8205d40045f77812"
        url = "https://api.segmind.com/v1/sdxl1.0-samaritan-3d"

        prompt = request.POST.get('user_prompt')

        data = {
          "prompt": prompt,
          "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly. young. long neck. (cross eyed:1.5). multiple characters",
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

            return render(request, 'result.html', context)

    return render(request, 'generate_image.html')





























#----------------------------------------------------------------------------

""" BASIC
from segmind import Kadinsky

api_key = "SG_8205d40045f77812"
model = Kadinsky(api_key)
img = model.generate("Dog with broccoli.")
img.show()
"""