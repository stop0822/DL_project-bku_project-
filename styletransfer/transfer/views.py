from sqlite3 import Time
from statistics import mode
from turtle import st
from django.shortcuts import render, redirect
import os
from PIL import Image
from .total_func import crystalize
from time import localtime
from django.http.response import StreamingHttpResponse
from .camera import FaceDetect

style_image_base_path = 'transfer/static/img/'
target_image_base_path = 'transfer/static/assets/'


def redirection(request):
    return redirect('/home')

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
        

        return redirect("/result/" + file_prefix)
        

    # if request.method == 'GET':
    #     return render(request,'main.html')
    if request.method == 'GET':
        # style 이미지의 이름만 가져오기
        style_image_list = os.listdir(style_image_base_path) # style 이미지 파일 리스트
        style_image_list = "".join(style_image_list)         # style 이미지 파일 이름들을 string 한줄로 합치기
        style_image_list = style_image_list.split('.jpg')    # style 이미지 .jpg 기준으로 split
        style_image_list = style_image_list[:-1]             # split() 된 list의 마지막 항목이 '' 으로 남아있으므로, 인덱싱으로 제외시키고 가져온다.

        # context를 이용해서 style_image_list를 templates에 넘겨준다.
        # dictionary의 key 값을 template의 jinja에서 찾는다.
        # dictionary의 value 값을 key로 찾은 templates에 넣어준다.
        # 따라서, template에 있는 style_image_list 라는 곳에
        # 'style 이미지의 이름만 가져오기'에서 만든 파이썬 변수인 style_image_list를 사용한다.
        return render(request,'main.html', {'style_image_list' : style_image_list})


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


def facedetect(request):
	return render(request, 'camera.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		
def facecam_feed(request):
	return StreamingHttpResponse(gen(FaceDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')