import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView
from face.forms import UploadImageForm
from face.models import Image, SubImage
import PIL
import cv2
from django.conf import settings
from django.db import models
import os
import numpy as np
from keras.models import model_from_json
from matplotlib import pyplot as plt
from keras.optimizers import SGD, sgd
from keras.models import Sequential
from django.core.files import File
from django.core.files.base import ContentFile

def list(request):
    context = Image.objects.all()
    return render(request, 'face/image_list.html', {'context': context})

def save_image_form(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.image = request.FILES['image']
            # img.slug = slug = ''.join(random.sample(string.ascii_lowercase, 6))
            img.save()
            extract_scores(img.id)
            # return render(request, 'face/image_scores.html', )
            return redirect('face/'+str(img.id)+'/')
    else:
        form = UploadImageForm()
    return render(request, 'face/image_form.html', {'form': form})

def detail(request, id):
    img = get_object_or_404(Image, pk=id)
    return render(request, 'face/image_scores.html', context={'image': img})

def extract_scores(id):
    img = Image.objects.get(pk=id)

    os.chdir(settings.MEDIA_ROOT)
    print(os.getcwd())
    imagePath = img.image.name
    print(imagePath)
    print(img.image.url)
    print(img.image.path)

    # Загрузка модель СНС
    class_names = ['Злость', 'Отвращение', 'Страх', 'Счастье', 'Грусть', 'Удивление', 'Нейтральная']
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights('model/checkpointBN-24-0.76-0.63-0.66-1.10.hdf5')
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    # Загрузка модель СНС

    # Обнаружение лица
    cascPath = "haarcascade/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(str(imagePath))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,  minNeighbors=5,  minSize=(30, 30))
    print("Found {0} faces!".format(len(faces)))
    # Обнаружение лица

    for (x, y, w, h) in faces:
        # Создаём объект модели для изображения
        sub_f = SubImage()
        sub_f.image = img

        sub_face = image[y:y + h, x:x + w]
        FaceFileName = 'unknowfaces/'+str(y)+'_'+imagePath
        cv2.imwrite(FaceFileName, sub_face)
        print(FaceFileName)
        sub_f.sub_image = FaceFileName

        # Определяем эмоции
        sub_face = cv2.resize(sub_face, (48, 48))
        sub_face = cv2.cvtColor(sub_face, cv2.COLOR_BGR2GRAY)
        pixel_face = np.asarray(sub_face)
        pixel_face = pixel_face / 255.0
        prediction = model.predict(pixel_face.reshape(1, 48, 48, 1))
        prediction = np.squeeze(prediction)

        scores_dict = dict.fromkeys(class_names)
        for i in range(len(class_names)):
            scores_dict[class_names[i]] = str('{0:.5f}'.format(prediction[i]))

        sub_f.scores = scores_dict
        sub_f.save()

        print(scores_dict)

    # return render(request, 'face/image_scores.html', context={'image': img})


