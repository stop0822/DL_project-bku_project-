from sqlite3 import Time
from django.shortcuts import render, redirect
import os
from PIL import Image
from .total_func import crystalize
from time import localtime
style_image_base_path = 'transfer/static/img/'
target_image_base_path = 'transfer/assets/'

def index(request):
    if request.method == 'POST':
        target_image = Image.open(request.FILES["target_img"])
        style_image = request.POST["style_img"]
        file_prefix = str(localtime().tm_year ) + str(localtime().tm_mon) + str(localtime().tm_mday) + str(localtime().tm_min) + str(localtime().tm_sec) 
        os.mkdir(target_image_base_path + file_prefix)
        target_image.save(target_image_base_path + file_prefix +'/target.jpg')
        target_path = target_image_base_path + file_prefix +'/target.jpg'
        
        style_path = style_image_base_path + style_image
        combination_image = crystalize(target_path, style_path)
        print(target_path,style_path)
        context = {'target_image':target_image,
                    'style_image':style_image}
                    #'combination':combination_image}
        return render(request,'main.html', context)

    if request.method == 'GET':

        return render(request,'main.html', {})
