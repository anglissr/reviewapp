# Defining forms that users can input data into in html files
from django import forms
from reviews.models import DISPLAYING, Review, RATINGS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ReviewForm, form that allows users to leave a review for a specific restaurant
class ReviewForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=False)
    # Added widget to allow styling
    text = forms.CharField(max_length=2500, required=True, help_text='Max 2500 Characters.', widget=forms.Textarea(attrs={'class':'review_field'}))
    rating = forms.ChoiceField(choices=RATINGS, required=True)

    class Meta:
        model = Review
        fields = ('username','text', 'rating')

# SignUpForm, allows users to create an account
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
class showForm(forms.ModelForm):
    display = forms.ChoiceField(choices=DISPLAYING, required=True)
    class Meta:
        model = Review
        fields = ('display',)