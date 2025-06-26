from django import forms
from books.models import BookReview

class AddReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')