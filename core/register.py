from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Clients
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Email Address"}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Last Name"}))
    contact = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Contact Number"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'contact')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

# Create the client form
class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}), label="")
    email = forms.EmailField(required=False, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}), label="")
    contact = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Contact'}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 1'}), label="")
    area = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 2'}), label="")
    suburb = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Suburb'}), label="")
    special_notes = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'placeholder':'Special Notes'}), label="")
    class Meta:
        model = Clients
        exclude = ('user',)