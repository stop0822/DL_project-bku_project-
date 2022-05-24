from django.shortcuts import render, redirect
import os
image_base_path = './static/img'

def index(request):
    if request.method == 'POST':
        target_image = request.FILES.getlist('img')
        style_image = request.POST['style_img']
        #combination_image = style_transfer(target_image,style_image)
        print(target_image)
        target_path = os.path.join(image_base_path , target_image)
        style_path = os.path.join(image_base_path , style_image)

        context = {'target_image':target_image,
                    'style_image':style_image}
                    #'combination':combination_image}
        return render(request,'main.html', context)

    if request.method == 'GET':

        return render(request,'main.html', {})
