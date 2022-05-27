from sqlite3 import Time
from statistics import mode
from django.shortcuts import render, redirect
import os
from PIL import Image
from .total_func import crystalize
from time import localtime
style_image_base_path = 'transfer/static/img/'
target_image_base_path = 'transfer/static/assets/'

def index(request):
    if request.method == 'POST':
        target_image = Image.open(request.FILES["target_img"],mode='r')
        style_image = request.POST["style_img"]
        file_prefix = str(localtime().tm_year ) + str(localtime().tm_mon) + str(localtime().tm_mday) + str(localtime().tm_min) + str(localtime().tm_sec) 
        os.mkdir(target_image_base_path + file_prefix)
        target_image.save(target_image_base_path + file_prefix +'/target.jpg')
        target_path = target_image_base_path + file_prefix +'/target.jpg'
        
        style_path = style_image_base_path + style_image + '.jpg'
        crystalize(target_path, style_path, target_image_base_path + file_prefix)
        combination_image = os.listdir('assets/' + file_prefix + '/')
        

        return render("/result/" + file_prefix)


    if request.method == 'GET':
        return render(request,'main.html')


def result(request,folder):
    folder = str(folder)
    print(folder)
    combination_image = os.listdir('transfer/static/assets/'+folder )
    print(combination_image)
    combination_image.remove('target.jpg')
    base_dir= 'assets/' + folder
    context = {'target': base_dir + '/' + 'target.jpg',
        'image_list':[ base_dir + '/' +x for x in combination_image]}


        
    return render(request,'result.html', context)



def home(request):

    return render(request,'home.html')

def readme(request):

    return render(request,'readme.html')

def developer(request):

    return render(request,'developer.html')