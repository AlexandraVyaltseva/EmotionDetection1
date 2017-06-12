from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Image
from django import forms

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        labels = {
            "image": "Щелкните здесь, чтобы загрузить изображение"
        }
