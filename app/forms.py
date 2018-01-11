from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
	class Meta:
		model   = Album
		exclude = []

	zip = forms.FileField(required=False)

#Custom Login Page (For Bride/Gromms login)
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AlbumUpdate(forms.ModelForm):
	class Meta:
		model   = Album
		exclude = []

	zip = forms.FileField(required=False)