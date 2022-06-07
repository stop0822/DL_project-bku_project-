from codecs import encode
import tensorflow as tf
import keras
tf.compat.v1.disable_eager_execution()
import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import save_img
from tensorflow.keras.preprocessing.image import load_img,img_to_array,save_img

import numpy as np
from keras.applications import vgg19  


#print(os.getcwd())
encoder = keras.models.load_model("model.h5",compile=True,options=None)
