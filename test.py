# -*- coding: utf-8 -*-  

'''
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
x_train = np.random.random((1000, 20))
y_train = np.random.randint(2, size=(1000, 1))
x_test = np.random.random((100, 20))
y_test = np.random.randint(2, size=(100, 1))

model = Sequential() 
model.add(Dense(64, input_dim=20, activation='relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(64, activation='relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy']) 
model.fit(x_train, y_train, epochs=20, batch_size=128) 
score = model.evaluate(x_test, y_test, batch_size=128)
'''

from __future__ import print_function
import numpy as np
np.random.seed(1337)

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

batch_size = 128
nb_classes = 10
nb_epoch = 12

# ����ͼ���ά�ȣ��˴���mnistͼ�������28*28
img_rows, img_cols = 28, 28
# �������ʹ�õľ���˵ĸ���
nb_filters = 32
# �ػ�������ķ�Χ
pool_size = (2,2)
# ����˵Ĵ�С
kernel_size = (3,3)
# keras�е�mnist���ݼ��Ѿ������ֳ���60,000��ѵ������10,000�����Լ�����ʽ�������¸�ʽ���ü���
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# ���ʹ��tensorflowʱ����tfģʽ�£�
# �Ὣ100��RGB��ͨ����16*32��ɫͼ��ʾΪ(100,16,32,3)��
# ��һ��ά��������ά����ʾ��������Ŀ��
# �ڶ��͵�����ά���ǸߺͿ�
# ���һ��ά����ͨ��ά����ʾ��ɫͨ����
X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

# ��X_train, X_test�����ݸ�ʽתΪfloat32
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# ��һ��
X_train /= 255
X_test /= 255
# ��ӡ�������Ϣ
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')


# ���������(��0��nb_classes����������)ӳ��Ϊ��ֵ������
# �൱�ڽ�������one-hot���±���
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# �������ģ��
model = Sequential()

# ����㣬�Զ�ά������л��������
# ��ʹ�øò�Ϊ��һ��ʱ��Ӧ�ṩinput_shape��������tfģʽ�У�ͨ��άλ�ڵ�����λ��
# border_mode���߽�ģʽ��Ϊ"valid","same"��"full"����ͼ����ı�Ե���ǲ�0
# ���ǲ�����ͬ���أ������ǲ�1
model.add(Convolution2D(nb_filters, kernel_size[0] ,kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
model.add(Activation('relu'))

# ����㣬�������ReLu
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))

# �ػ��㣬ѡ��Maxpooling������pool_size��dropout����Ϊ0.25
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(0.25))

# Flatten�㣬�Ѷ�ά�������һά���������ھ���㵽ȫ���Ӳ�Ĺ���
model.add(Flatten())

# ����128����Ԫ��ȫ���Ӳ㣬�����ΪReLu��dropout����Ϊ0.5
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))

# ����10����Ԫ������㣬�����ΪSoftmax
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# ���ģ�͵Ĳ�����Ϣ
model.summary()
# ����ģ�͵�ѧϰ����
model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])
# ѵ��ģ��
model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))

# ��batch������ĳЩ����������ģ�͵����
score = model.evaluate(X_test, Y_test, verbose=0)
# ���ѵ���õ�ģ���ڲ��Լ��ϵı���
print('Test score:', score[0])
print('Test accuracy:', score[1])