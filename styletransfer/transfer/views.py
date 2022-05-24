from django.shortcuts import render, redirect
import os
from PIL import Image
image_base_path = './static/img'

def index(request):
    if request.method == 'POST':
        target_image = Image.open(request.FILES["target_img"])
        style_image = request.POST['style_img']
        target_image.show()
        #combination_image = style_transfer(target_image,style_image)
        print(target_image)
        target_path = os.path.join(image_base_path , str(target_image))
        style_path = os.path.join(image_base_path , str(style_image))
        print(target_path,style_path)
        context = {'target_image':target_image,
                    'style_image':style_image}
                    #'combination':combination_image}
        return render(request,'main.html', context)

    if request.method == 'GET':

        return render(request,'main.html', {})
