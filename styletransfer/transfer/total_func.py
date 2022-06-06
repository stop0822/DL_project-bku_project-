import tensorflow as tf
tf.compat.v1.disable_eager_execution()

from tensorflow.keras.preprocessing.image import save_img
from tensorflow.keras.preprocessing.image import load_img,img_to_array,save_img

import numpy as np
from keras.applications import vgg19
from keras import backend as K

from scipy.optimize import fmin_l_bfgs_b
import time


# 사용자 정의 함수 -----------------------------------------

# 전역변수를 설정해준다.
# 단, target_image_path, style_reference_image_path 전역변수에는 target_경로, style_경로를 입력으로 받는다.
# 다른 함수들에서 img_height, img_width 를 사용하기 때문에 global 변수로 지정
# 경로를 입력받아 사진의 height, width 를 return 하는 함수.
# 다른 사용자 함수들에서 참조하여 사용하기 때문에 만들어졌음.
def get_height_width(target_img_path, style_reference_img_path):
    # global(전역변수)로 설정
    global target_image_path
    global style_reference_image_path

    # 전역변수 = 입력 받는 값(함수에서 입력받은 input 값)
    # 입력 받는 값은
    #   1. 사용자가 올릴 사진
    #   2. 스타일 사진
    target_image_path = target_img_path
    style_reference_image_path = style_reference_img_path
    
    width,height = load_img(target_image_path).size
    
    img_height = 400
    img_width = int(width * img_height / height)
    
    return img_height, img_width


def preprocess_image(image_path):
    # target_size=(img_height, img_width) 형태이므로
    # img_height, img_width를 튜플으로 반환하는 get_height_width(target_image_path, style_reference_image_path) 함수를 그대로 사용.
    img = load_img(image_path, target_size=get_height_width(target_image_path, style_reference_image_path))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img


def deprocess_image(x):
    # ImageNet의 평균 픽셀 값을 더한다.
    # vgg19.preprocess_input 함수에서 일어나는 변환을 복원한다.
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    
    # vgg19.preprocess_input 함수에서 일어나는 변환을 복원하기 위한 것이다.
    x = x[:, :, ::-1] #BGR -> RGB로 변환
    x = np.clip(x, 0, 255).astype('uint8')
    return x


# <콘텐츠 손실>
# VGG19 컨브넷의 상위 층(target과 가까운 쪽)은
# 타깃 이미지(입력 받은 사진)와 생성된 이미지를 동일하게 바라보아야 한다.
def content_loss(base, combination) :
    return K.sum(K.square(combination - base))

# 그람 매트릭스는 특성 맵들의 내적이다.
# 내적은 층의 특성 사이에 있는 상관관계를 표현한다.
# 특성의 상관관계는 특정 크기의 공간적인 패턴 통계를 잡아낸다.
def gram_matrix(x) :
    features = K.batch_flatten(K.permute_dimensions(x, (2,0,1)))
    gram = K.dot(features, K.transpose(features))
    return gram

# 스타일 참조 이미지와 생성된 이미지로 층의 활성화를 계산한다.
# 스타일 손실은 그 안에 내재된 상관관계를 비슷하게 보존하는 것이 목적이다.
# 스타일 참조 이미지와 생성된 이미지에서 여러 크기의 텍스처가 비슷하게 보이도록 만든다.
def style_loss(style, combination) :
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = get_height_width(target_image_path, style_reference_image_path)[0] * get_height_width(target_image_path, style_reference_image_path)[1]
    return K.sum(K.square(S - C)) / (4. * (channels ** 2) * (size ** 2))


# 총 변위 손실
# 생성된 이미지가 공간적인 연속성을 가지도록 도와주며 픽셀의 격자무늬가 과도하게 나타나는 것을 막아준다.
# 규제항으로 생각하면 이해하기 편한다.
def total_variation_loss(x) :
    a = K.square(
            x[:, :get_height_width(target_image_path, style_reference_image_path)[0] - 1, :get_height_width(target_image_path, style_reference_image_path)[1] - 1, :] - x[:, 1:, :get_height_width(target_image_path, style_reference_image_path)[1] -1, :]
        ) 

    b = K.square(
            x[:, :get_height_width(target_image_path, style_reference_image_path)[0] - 1, :get_height_width(target_image_path, style_reference_image_path)[1] - 1, :] - x[:, :get_height_width(target_image_path, style_reference_image_path)[0] - 1, 1:, :]
        )
    
    return K.sum(K.pow(a + b, 1.25))

# 최소화할 손실은
# content_loss, style_loss, total_variation_loss 
# 세 가지 손실의 가중치 평균이다.

# ---------------------------------------------------
class Evaluator(object):
    def __init__(self):
        self.loss_value = None
        self.grads_values = None
        
    def loss(self, x):
        assert self.loss_value is None
        # x = x.reshape((1, img_height, img_width, 3))
        x = x.reshape((1, get_height_width(target_image_path, style_reference_image_path)[0], get_height_width(target_image_path, style_reference_image_path)[1], 3))
        outs = fetch_loss_and_grads([x])
        loss_value = outs[0]
        grad_values = outs[1].flatten().astype('float64')
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value
    
    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values


# ---------------------------------------------------------
              # target_img_path 는 str 형태의 경로
                               # style_reference_image_path 는 str 형태의 경로
def crystalize(target_img_path, style_reference_img_path,file_prefix) :
   
    # global 변수 target_image_path, style_reference_image_path 선언
    # 함수에 들어가는 input에는 img
    # 함수가 실행된 뒤, 생성되는 변수는 image 가 들어간다.
    get_height_width(target_img_path, style_reference_img_path)

    # 
    target_image = K.constant(preprocess_image(target_image_path))
    style_reference_image = K.constant(preprocess_image(style_reference_image_path))
    combination_image = K.placeholder((1,get_height_width(target_image_path, style_reference_image_path)[0],get_height_width(target_image_path, style_reference_image_path)[1],3))

    # tensor들을 다 합친다.
    input_tensor = K.concatenate([target_image,
                                style_reference_image,
                                combination_image],axis=0)

    # vgg19 모델을 생성한다.
    # 이 때, 분류기는 제외시켜서 컨브넷만 가져온다.
    model = vgg19.VGG19(input_tensor=input_tensor,
                        weights='imagenet',
                        include_top=False)

    # vgg19 모델의 각 층의 이름과 결과를 딕셔너리 형태로 받는다.
    outputs_dict = dict([ (layer.name, layer.output) for layer in model.layers ])
    
    # 원하는 레이어를 선택
    content_layer = 'block5_conv2'
    style_layers = ['block1_conv1',
                    'block2_conv1',
                    'block3_conv1',
                    'block4_conv1',
                    'block5_conv1'
                    ]


    # 손실 항목의 가중치 평균에 사용할 가중치이다.
    # 스케일을 맞춰주기 위해서 사용한다. 
    total_variation_weight = 1e-4
    style_weight = 1.
    content_weight = 0.025

    loss = K.variable(0.)
    
    # 
    layer_features = outputs_dict[content_layer]
    target_image_features = layer_features[0, :, :, :]
    combination_features = layer_features[2, :, :, :]
    
    # 사용자 정의함수인 content_loss 사용
    loss = loss + content_weight * content_loss(target_image_features, combination_features)

    for layer_name in style_layers :
        layer_features = outputs_dict[layer_name]
        style_reference_features = layer_features[1, :, :, :]
        combination_features = layer_features[2, :, :, :]
        sl = style_loss(style_reference_features, combination_features)
        loss = loss + (style_weight / len(style_layers)) * sl
        
        
    loss = loss + total_variation_weight * total_variation_loss(combination_image)



    grads = K.gradients(loss, combination_image)[0]

    # Evaluator() class의 loss에서 outs 변수를 만들 때 사용된다.
    # global(전역 변수) 안넣어주면 에러 발생해서 넣어줬다.
    global fetch_loss_and_grads
    fetch_loss_and_grads = K.function([combination_image], [loss, grads])
    
    evaluator = Evaluator()

    result_prefix = 'style_transfer_result'
    iterations = 6

    x = preprocess_image(target_image_path)
    x = x.flatten()
    for i in range(iterations):
        print('반복 횟수 : ', i)
        start_time = time.time()
        x, min_val, info = fmin_l_bfgs_b(evaluator.loss,
                                        x,
                                        fprime = evaluator.grads,
                                        maxfun = 20)
        print('현재 손실 값 : ', min_val)
        img = x.copy().reshape((get_height_width(target_image_path, style_reference_image_path)[0], get_height_width(target_image_path, style_reference_image_path)[1], 3))
        img = deprocess_image(img)
        
        # fname은 file name 이다.
        fname = file_prefix + '/' +result_prefix + '_at_iteration_%d.png' % i
        save_img(fname, img)
        print('저장 이미지 : ', fname)
        end_time = time.time()
        print('%d 번째 반복 완료 : %ds' % (i, end_time - start_time))
        
    return None

# ----------------------------------------------------------------------------------
