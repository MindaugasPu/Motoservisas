from .models import UzsakymoReview
from django import forms

class UzsakymoReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymoReview
        fields = ('content', 'uzsakymas', 'reviewer',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}