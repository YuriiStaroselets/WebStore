from django import forms
from store.models import Carousel


class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['category', 'title', 'banner_image', 'is_available']
