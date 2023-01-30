from .models import UzsakymoReview, Profilis
from django import forms
from django.contrib.auth.models import User

class UzsakymoReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymoReview
        fields = ('content', 'uzsakymas', 'reviewer',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']
