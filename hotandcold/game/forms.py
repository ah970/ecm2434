from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class EventCreationForm(forms.Form):
    title = forms.CharField(label="Title", max_length=80)
    description = forms.CharField(label="Description", max_length=200)

    start = forms.DateTimeField(label="Start")
    end = forms.DateTimeField(label="End")

    latitude = forms.DecimalField(label="Latitude", max_digits=22, decimal_places=16)
    longitude = forms.DecimalField(label="Longitude", max_digits=22, decimal_places=16)
